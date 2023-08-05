#!/usr/bin/python

# TODO:
# - do not rely on node name for getting all nodes. Use meta properties.


import sys
from argparse import ArgumentParser
import os
import yaml
import json
import zipfile
from datetime import datetime
import operator
from collections import Counter
import string
import random
import shutil
import hashlib
#import ipdb

from jinja2 import Environment, FileSystemLoader
from openapi_spec_validator.exceptions import OpenAPIValidationError
import numpy as np
#import spacy

from cvsvc_apirisk.score.spec_security.sps_main import SpecSecMain
from cvsvc_apirisk.score.spec_security.sps_main_cr import SpecSecCustomRulesMain
from cvsvc_apirisk.score.spec_security.sps_common import \
        SEVERITY_CTGS, get_severity, init_rules_ds
from cvsvc_apirisk.score.spec_security.sps_common import get_api2 as api_fn
from cvsvc_apirisk.score.spec_security.sps_common import get_api2_op as api_op_fn
from cvsvc_apirisk.score.spec_security.sps_common import get_api2_param as api_param_fn
from cvsvc_apirisk.score.spec_security.json_line import SaveLineRangeDecoder


UNZIP_DIR = '/tmp/cvapispecrisk_'
# https://spacy.io/api/annotation#pos-tagging
EXCL_POS = set(['NUM', 'PROPN', 'PUNCT', 'X', 'SYM', 'SPACE', 'NOUN'])
qspecs = {}


def print_heading(title):
    print()
    print(title)
    print('-'*len(title))
    return


def check_one_spec(abs_path, report, cvrules_path, rules_path=None):
    target_obj = {}

    print('-'*10)
    print('- Analyzing %s...' % abs_path)
    with open(abs_path) as inf:
        report['files'][abs_path] = {}
        try:
            if abs_path.endswith('.json'):
                raw_spec = json.load(inf)
                inf.seek(0)
                linenum_mapping = json.load(inf, cls=SaveLineRangeDecoder)
            elif abs_path.endswith('.yaml'):
                raw_spec = yaml.safe_load(inf)
                linenum_mapping = None
            else:
                raise ValueError('Incorrect input file. Should be JSON/YAML.')

            #ipdb.set_trace()

            # Check whether OpenAPI v2 or v3
            if 'swagger' in raw_spec:
                openapi_ver = 'v2'
            elif 'openapi' in raw_spec:
                openapi_ver = 'v3'
            else:
                raise ValueError('Incorrect specification format')

            target_obj['raw_spec'] = raw_spec
            spec_main_cr = \
                    SpecSecCustomRulesMain(target_obj=target_obj,
                                           linenum_mapping=linenum_mapping,
                                           openapi_ver=openapi_ver)

            rule_exps = {}
            for rules_file in filter(None, [cvrules_path, rules_path]):

                if rules_file.endswith('.txt'):
                    rule_exps1 = spec_main_cr.read_rules_raw(rules_file)
                elif rules_file.endswith('.json'):
                    rule_exps1 = spec_main_cr.read_rules_json(rules_file)
                rule_exps.update(rule_exps1)

            spec_main_cr.analyze_rules(rule_exps)
            spec_main = spec_main_cr.spec_main

            global RISK_CTGS, RISK_SUBCTGS

            RISK_CTGS, RISK_SUBCTGS = init_rules_ds(rule_exps)
            report['files'][abs_path]['status'] = 'valid'
            report['files'][abs_path]['score'] = spec_main.score
            report['files'][abs_path]['meta'] = spec_main.meta
            report['files'][abs_path]['num_apis'] = \
                            len(spec_main.qspec.spec_obj['paths'])
            report['files'][abs_path]['num_params'] = \
                            len(spec_main.qspec.get_param_objs()[0])
            report['files'][abs_path]['version'] = \
                            target_obj['raw_spec']['info']['version']
            report['files'][abs_path]['num_evaluations'] = \
                            spec_main_cr.num_evaluations
            report['files'][abs_path]['req_method'] = spec_main.qspec.get_method_objs()
            report['files'][abs_path]['response_codes'] = spec_main.qspec.get_response_objs()[1]
            report['files'][abs_path]['data_types'] = spec_main.qspec.get_param_objs()[1]

            qspecs[abs_path] = spec_main.qspec

            # Init API data structures
            report['files'][abs_path]['apis'] = {}
            for api_url in spec_main.qspec.spec_obj['paths']:
                api = abs_path.split('/')[-1] + ':' + api_url
                init_api_ds(report, abs_path, api)

        except OpenAPIValidationError as e:
            report['files'][abs_path]['status'] = 'err'
            report['files'][abs_path]['meta'] = str(e)
            print('-> Error encountered for ', abs_path)

    return


def check_specs(spec_zip, cvrules_path, rules_path=None):
    report = {}

    # Get the filename
    report['file_name'] = spec_zip

    # Get the file timestamp
    report['file_modified_time'] = \
        str(datetime.fromtimestamp(int(os.path.getmtime(spec_zip))))

    # Unzip the zip file
    unzip_dir = '%s%s' % (UNZIP_DIR,
                          ''.join(random.sample(string.ascii_lowercase, 4)))
    with zipfile.ZipFile(spec_zip) as zipf:
        zipf.extractall(unzip_dir)

    report['pdf'] = {}
    report['pdf']['page1'] = {}

    report['files'] = {}
    for filename in os.listdir(unzip_dir):
        # TODO: find all files which are yaml/json
        abs_path = '%s/%s' % (unzip_dir, filename)
        check_one_spec(abs_path, report, cvrules_path, rules_path=rules_path)

    return report, unzip_dir


def analyze_apps(report):

    print_heading('App analysis')

    report['pdf']['page1']['sec2'] = {}

    ## Top-level app insights
    # Risk defined across all services
    risk_scores = [report['files'][f]['score'] for f in report['files'] \
                                            if 'score' in report['files'][f]]
    report['max_risk'] = max(risk_scores)
    print(('* Max risk across all application services:\t%d (%s)' %
           (report['max_risk'], get_severity(report['max_risk']))).expandtabs(20))

    # Risk statistics
    report['avg_risk'] = round(np.mean(risk_scores), 2)
    print(('* Average risk across all application services:\t%d' %
           report['avg_risk']).expandtabs(20))

    num_nz_risk = len(list(filter(lambda x: x > 0, risk_scores)))
    print(('* Number of application services with non-zero risk:\t%d' %
           num_nz_risk).expandtabs(20))
    num_z_risk = len(list(filter(lambda x: x == 0, risk_scores)))
    print(('* Number of application services with zero risk:\t%d' %
           num_z_risk).expandtabs(20))

    # Initialize the data structure
    report['pdf']['page1']['sec2']['2a'] = {}

    severities = []
    file_severities = []
    for f in report['files']:
        if report['files'][f]['status'] == 'err':
            continue
        severities.append(get_severity(report['files'][f]['score']))
        file_severities.append((f, report['files'][f]['score']))
    print('* Number of application services by Severity:')
    #for k, v in Counter(severities).items():
    ctr = Counter(severities)
    for k in SEVERITY_CTGS:
        print(('\t%s\t%d' % (k, ctr[k])).expandtabs(10))
        report['pdf']['page1']['sec2']['2a'][k] = ctr[k]

    print('* Top 5 application services ranked by Severity:')
    for f, score in sorted(file_severities, key=operator.itemgetter(1),
            reverse=True)[:5]:
        print(('    %s\t%s' % (f.split('/')[-1],
                               get_severity(score))).expandtabs(20))


    app_severity_riskctg = {}
    app_severity_risksubctg = {}
    ## Severity/Category-based app insights
    for f in report['files']:
        if report['files'][f]['status'] == 'err':
            continue

        if f not in app_severity_riskctg:
            app_severity_riskctg[f] = {}
            app_severity_risksubctg[f] = {}

        #for attr_score, remed_clue in report['files'][f]['meta']:
        for v in report['files'][f]['meta']:
            severity = get_severity(v['v_score'])

            if severity not in app_severity_riskctg[f]:
                app_severity_riskctg[f][severity] = {}
                app_severity_risksubctg[f][severity] = {}

            risk_ctg, risk_subctg = v['v_risk_ctg'], v['v_risk_subctg']
            if risk_ctg not in app_severity_riskctg[f][severity]:
                app_severity_riskctg[f][severity][risk_ctg] = 0
                app_severity_risksubctg[f][severity][risk_ctg] = {}

            # Log the violation
            app_severity_riskctg[f][severity][risk_ctg] += 1

            if risk_subctg is not None:
                if risk_subctg not in \
                        app_severity_risksubctg[f][severity][risk_ctg]:
                    app_severity_risksubctg[f][severity][risk_ctg][risk_subctg] = 0
                app_severity_risksubctg[f][severity][risk_ctg][risk_subctg] += 1

        # report['app_severity_riskctg'] = app_severity_riskctg

    print('* Number of application services by RiskCategory-Severity:')
    severity_ctg_cnts = {}
    for f in app_severity_riskctg:
        for severity in app_severity_riskctg[f]:
            if severity not in severity_ctg_cnts:
                severity_ctg_cnts[severity] = {}
            for risk_ctg in app_severity_riskctg[f][severity]:
                if risk_ctg not in severity_ctg_cnts[severity]:
                    severity_ctg_cnts[severity][risk_ctg] = 0
                severity_ctg_cnts[severity][risk_ctg] += 1

    report['pdf']['page1']['sec2']['2b'] = {}
    # Initialize the data structure
    for sev in SEVERITY_CTGS:
        report['pdf']['page1']['sec2']['2b'][sev] = {}
        for risk in RISK_CTGS:
            report['pdf']['page1']['sec2']['2b'][sev][risk] = 0

    # Now print
    for severity in sorted(severity_ctg_cnts, key=lambda s: SEVERITY_CTGS[s]):
        for ctg in sorted(severity_ctg_cnts[severity],
                          key=lambda r: RISK_CTGS[r]):
            print(('    %s\t%s\t%d' % (severity, ctg,
                            severity_ctg_cnts[severity][ctg])).expandtabs(20))
            report['pdf']['page1']['sec2']['2b'][severity][ctg] = \
                severity_ctg_cnts[severity][ctg]
    return


def analyze_apis_riskctg(report, api_riskctg_severity):

    report['pdf']['page1']['sec3']['3b'] = {}
    # Initialize the data structure
    for sev in SEVERITY_CTGS:
        report['pdf']['page1']['sec3']['3b'][sev] = {}
        for risk in RISK_CTGS:
            report['pdf']['page1']['sec3']['3b'][sev][risk] = 0

    print('* Number of APIs by RiskCategory-Severity:')
    #for riskctg, severity_dict in api_riskctg_severity.items():
    for riskctg in sorted(api_riskctg_severity, key=lambda r: RISK_CTGS[r]):
        severity_dict = api_riskctg_severity[riskctg]
        #for severity in severity_dict:
        for severity in sorted(severity_dict, key=lambda s: SEVERITY_CTGS[s]):
            print(('    %s\t%s\t%d' % (severity, riskctg,
                        len(severity_dict[severity]['apis']))).expandtabs(20))
            report['pdf']['page1']['sec3']['3b'][severity][riskctg] = \
                        len(severity_dict[severity]['apis'])

    '''
    report['pdf']['page1']['sec3']['3c'] = {}
    # Initialize the data structure
    for sev in SEVERITY_CTGS:
        report['pdf']['page1']['sec3']['3c'][sev] = {}
        for risk in ['AuthN/AuthZ', 'API Transport']:
            report['pdf']['page1']['sec3']['3c'][sev][risk] = {}
            for subctg in RISK_SUBCTGS[risk]:
                report['pdf']['page1']['sec3']['3c'][sev][risk][subctg] = 0
    '''

    print('* Number of APIs by RiskCategory-Severity-RiskSubCategory:')
    #for riskctg, severity_dict in api_riskctg_severity.items():
    for riskctg in sorted(api_riskctg_severity, key=lambda r: RISK_CTGS[r]):
        severity_dict = api_riskctg_severity[riskctg]
        #for severity in severity_dict:
        for severity in sorted(severity_dict, key=lambda s: SEVERITY_CTGS[s]):
            for risksubctg, apilist in \
                    severity_dict[severity]['subctgs'].items():
                print(('    %s\t%s\t%s\t%d' % (severity, riskctg, risksubctg,
                                             len(apilist))).expandtabs(20))
    '''
                report['pdf']['page1']['sec3']['3c'][severity][riskctg][risksubctg] = \
                                             len(apilist)
    '''

    return


def analyze_apis_uniq_severity_old(report, api_riskctg_severity):

    api_severity = Counter()
    for f in report['files']:
        if report['files'][f]['status'] == 'err':
            continue
        for api in report['files'][f]['apis']:
            ctr = Counter(report['files'][f]['apis'][api]['severities'])
            for severity in ctr:
                api_severity[severity] += 1

    print('* Number of APIs by Severity:')
    #for k, v in api_severity.items():
    #for severity in sorted(api_severity, key=lambda s: SEVERITY_CTGS[s]):
    #for severity in SEVERITY_CTGS:
    for severity in sorted(api_severity, key=lambda s: SEVERITY_CTGS[s]):
        print(('    %s\t%d' % (severity, api_severity[severity])).expandtabs(20))
        #print(('    %s\t%d' % (severity, api_severity.get(severity,
        #                                                  0))).expandtabs(20))

    analyze_apis_riskctg(api_riskctg_severity)

    return


def analyze_apis_uniq_api_new(report, api_riskctg_severity):

    severity_cntr = Counter()
    for f in report['files']:
        if report['files'][f]['status'] == 'err':
            continue
        for api in report['files'][f]['apis']:
            max_score = max([v['v_score'] for v in \
                                report['files'][f]['apis'][api]['meta']],
                            default=0)
            max_score_severity = get_severity(max_score)
            severity_cntr[max_score_severity] += 1

    report['pdf']['page1']['sec3']['3a'] = {}
    # Initialize the data structure
    for sev in SEVERITY_CTGS:
        report['pdf']['page1']['sec3']['3a'][sev] = 0

    print('* Number of APIs by Severity:')
    for severity in sorted(severity_cntr, key=lambda s: SEVERITY_CTGS[s]):
        print(('    %s\t%d' % (severity, severity_cntr[severity])).expandtabs(20))
        report['pdf']['page1']['sec3']['3a'][severity] = severity_cntr[severity]

    if 'NoRisk' not in severity_cntr:
        total_violated_apis = sum(severity_cntr.values())
        num_norisk_apis = report['total_apis'] - total_violated_apis
        print(('    %s\t%d' % ('NoRisk', num_norisk_apis)).expandtabs(20))
        report['pdf']['page1']['sec3']['3a']['NoRisk'] = num_norisk_apis

    analyze_apis_riskctg(report, api_riskctg_severity)

    return


def init_api_ds(report, f, api):
    report['files'][f]['apis'][api] = {}
    #report['files'][f]['apis'][api]['severities'] = []
    #report['files'][f]['apis'][api]['risk_ctg'] = []
    #report['files'][f]['apis'][api]['risk_subctg'] = []
    report['files'][f]['apis'][api]['meta'] = []
    return


def analyze_apis(report):

    print_heading('API analysis')

    report['pdf']['page1']['sec3'] = {}

    api_riskctg_severity = {}
    ## Severity/Category-based API insights
    for f in report['files']:
        if report['files'][f]['status'] == 'err':
            continue

        # for attr_score, remed_clue in report['files'][f]['meta']:
        for v in report['files'][f]['meta']:
            remed_clue = '%s %s %s' % (v['v_ruleid'], v['v_entity'],
                                       v['v_description'])
            api = api_fn(remed_clue)
            if api is None:
                continue
            api = f.split('/')[-1] + ':' + api
            if api not in report['files'][f]['apis']:
                init_api_ds(report, f, api)

            report['files'][f]['apis'][api]['meta'].append(v)

            severity = get_severity(v['v_score'])
            #report['files'][f]['apis'][api]['severities'].append(severity)
            risk_ctg, risk_subctg = v['v_risk_ctg'], v['v_risk_subctg']
            #report['files'][f]['apis'][api]['risk_ctg'].append(risk_ctg)
            #if risk_subctg is not None:
            #    report['files'][f]['apis'][api]['risk_subctg'].append(risk_subctg)

            if risk_ctg not in api_riskctg_severity:
                api_riskctg_severity[risk_ctg] = {}
            if severity not in api_riskctg_severity[risk_ctg]:
                api_riskctg_severity[risk_ctg][severity] = {}
                api_riskctg_severity[risk_ctg][severity]['apis'] = set()
                api_riskctg_severity[risk_ctg][severity]['subctgs'] = {}
            api_riskctg_severity[risk_ctg][severity]['apis'].add(api)
            if risk_subctg is not None:
                if (risk_subctg not in
                     api_riskctg_severity[risk_ctg][severity]['subctgs']):
                    api_riskctg_severity[risk_ctg][severity]['subctgs'][risk_subctg] =  set()
                api_riskctg_severity[risk_ctg][severity]['subctgs'][risk_subctg].add(api)

    #analyze_apis_uniq_severity_old(report, api_riskctg_severity)

    analyze_apis_uniq_api_new(report, api_riskctg_severity)

    #return api_riskctg_severity

    return


def common_themes(report, nlp):

    print_heading('Common themes')

    report['pdf']['page1']['sec5'] = {}

    # Theme 1: Most frequently occuring violation

    violation2file = {}
    for f in report['files']:
        if report['files'][f]['status'] == 'err':
            continue

        for v in report['files'][f]['meta']:
            code_str = '[%s] %s' % (v['v_ruleid'], v['v_description'])
            if code_str not in violation2file:
                violation2file[code_str] = []
            violation2file[code_str].append(f)

    most_frq_code = None
    max_frq = 0
    for code in violation2file:
        if len(violation2file[code]) > max_frq:
            most_frq_code = code
            max_frq = len(violation2file[code])

    if most_frq_code is not None:
        p1_1_text = '* Most frequently occuring violation:\t%s (%d)' % \
                                (most_frq_code, max_frq)
        print(p1_1_text.expandtabs(10))


        # Find the corresponding file
        file_ctr = sorted(Counter(violation2file[most_frq_code]).items(),
                          key=operator.itemgetter(1), reverse=True)
        most_frq_file, file_frq = file_ctr[0]
        p1_2_text = 'App with the largest number of this violation: %s (%d)' %\
                                    (most_frq_file.split('/')[-1], file_frq)

        report['pdf']['page1']['sec5']['p1'] = p1_1_text + p1_2_text

    # Theme 2: Apps with multiple RiskSubCtg
    file2subctg = {}
    for f in report['files']:
        if report['files'][f]['status'] == 'err':
            continue

        file2subctg[f] = {}
        #for attr_score, remed_clue in report['files'][f]['meta']:
        for v in report['files'][f]['meta']:
            risk_ctg, risk_subctg = v['v_risk_ctg'], v['v_risk_subctg']
            if risk_subctg is None:
                continue
            if risk_subctg not in file2subctg:
                file2subctg[f][risk_subctg] = 0
            file2subctg[f][risk_subctg] += 1

    intr_files = []
    for f in file2subctg:
        if (('Authorization' in file2subctg[f]) and
                ('Authentication' in file2subctg[f])):
            cnt = file2subctg[f]['Authorization'] + \
                        file2subctg[f]['Authentication']
            intr_files.append((f, cnt))
    sorted_intr_files = sorted(intr_files, key=operator.itemgetter(1),
                               reverse=True)

    if len(sorted_intr_files) > 0:
        p2_text = '* %d application service(s) contain both Authorization and '\
              'Authentication based Security violations. Most violations occur'\
              ' for the app: %s.' % (len(intr_files),
                                     sorted_intr_files[0][0].split('/')[-1])
        print(p2_text)
        report['pdf']['page1']['sec5']['p2'] = p2_text

    # Description stats
    #get_description_stats(report, nlp)
    return


def high_level_info(report):

    print_heading('Basic information')

    ## High level info
    print(('* Zip file name:\t%s' % report['file_name']).expandtabs(80))
    print(('* Zip file uploaded on:\t%s' % report['file_modified_time']).expandtabs(80))
    report['num_appsvcs'] = len(report['files'])

    total_files = 0
    total_apis = 0
    total_params = 0
    total_violations = 0
    total_evaluations = 0
    for f in report['files']:
        if report['files'][f]['status'] == 'err':
            continue
        total_files += 1
        total_apis += report['files'][f]['num_apis']
        total_params += report['files'][f]['num_params']
        total_violations += len(report['files'][f]['meta'])
        total_evaluations += report['files'][f]['num_evaluations']

    print(('* Total number of application services:\t%d' %
           total_files).expandtabs(80))
    report['total_apis'] = total_apis
    print(('* Total number of APIs observed across all services:\t%d' %
           report['total_apis']).expandtabs(80))

    #print(('* Total number of Parameters observed across all services:\t%d' %
    #       total_params).expandtabs(80))

    print(('* Total number of violations across all services:\t%d (out of'
           ' %d checks)' %
           (total_violations, total_evaluations)).expandtabs(80))
    report['pdf']['page1']['sec4'] = {}
    report['pdf']['page1']['sec4']['total_violations'] = total_violations
    report['pdf']['page1']['sec4']['total_evaluations'] = total_evaluations

    # Top 5 apps by APIs
    print('* Top 5 application services by num APIs')
    #return report
    data = sorted({k: v['num_apis'] for k, v in report['files'].items() \
                                        if 'num_apis' in v}.items(),
                  key=operator.itemgetter(1), reverse=True)
    for filename, num_apis in data[:5]:
        print(('    %s\t%d' % (filename.split('/')[-1], num_apis)).expandtabs(40))

    return


def insights(report):

    print_heading('Insights')

    api2op = {}
    api2params = {}
    for f in report['files']:
        if report['files'][f]['status'] == 'err':
            continue

        #for attr_score, remed_clue in report['files'][f]['meta']:
        for v in report['files'][f]['meta']:
            remed_clue = '%s %s %s' % (v['v_ruleid'], v['v_entity'],
                                       v['v_description'])
            api = api_fn(remed_clue)
            if api is None:
                continue
            api = f.split('/')[-1] + ':' + api
            #print(api)
            if api not in api2op:
                api2op[api] = {}
                api2params[api] = {}

            api_op = api_op_fn(remed_clue)
            api_param = api_param_fn(remed_clue)

            if api_param is not None:
                api2params[api][api_param] = True

            #print(api_op)
            #print(attr_score)
            #print(remed_clue)
            severity = get_severity(v['v_score'])
            if severity == 'Critical' and api_op in ('post', 'put'):
                api2op[api]['postput'] = 1
            if severity == 'Critical' and api_op in ('get', 'post'):
                api2op[api]['getpost'] = 1

    if len(api2op) > 0:
        # 1. POST/PUT
        num = len([a for a in api2op if 'postput' in api2op[a]])
        den = len(api2op)
        perc1 = num*100.0/den
        if perc1 > 0.0:
            data_in_text = '* %02d%% of APIs have Critical violations among'\
                'POST/PUT operations which bring data into your environment.' % perc1
            print(data_in_text)
            report['pdf']['page1']['sec4']['data_in'] = data_in_text

        # 2. GET/POST
        num = len([a for a in api2op if 'getpost' in api2op[a]])
        den = len(api2op)
        perc2 = num*100.0/den
        if perc2 > 0.0:
            data_out_text = '* %02d%% of APIs have Critical violations among'\
                'GET/POST operations which pull data out of your environment.' % perc2
            print(data_out_text)
            report['pdf']['page1']['sec4']['data_out'] = data_out_text

    if len(api2params) > 0:
        #print(api2params)
        # 3. Num of APIs with high param violations
        num = len([a for a in api2params if len(api2params[a]) > 3])
        den = len(api2params)
        perc3 = num*100.0/den
        if perc3 > 0.0:
            problem_parameters = '* %02d%% of APIs have more than 3 '\
                'parameters that have contributed to a violation.' % perc3
            print(problem_parameters)
            report['pdf']['page1']['sec4']['problem_parameters'] = problem_parameters

    return


def print_samples(report, spec_path):
    f = spec_path
    print('-'*100)
    print('Spec: %s\n' % f)

    if report['files'][f]['status'] == 'err':
        return

    grouped_violations = {}
    for v in report['files'][f]['meta']:
        remed_clue = '%s %s %s' % (v['v_ruleid'], v['v_entity'],
                                   v['v_description'])
        api = api_fn(remed_clue)
        if api not in grouped_violations:
            grouped_violations[api] = []
        grouped_violations[api].append(v)

    # Print the global violations first
    if None in grouped_violations:
        for v in grouped_violations.get(None):
            print('-'*20)
            print(('\t%s\n\t%d\t%s\t%s\n\t%s' % (v['v_description'],
                                                 v['v_score'],
                                                 get_severity(v['v_score']),
                                                 v['v_ruleid'],
                                                 v['v_entity']
                                                 )).expandtabs(10))
        del(grouped_violations[None])

    for api in grouped_violations:
        for v in grouped_violations[api]:
            print('-'*20)
            print(('\t%s\n\t%d\t%s\t%s\n\t%s' % (v['v_description'],
                                                 v['v_score'],
                                                 get_severity(v['v_score']),
                                                 v['v_ruleid'],
                                                 v['v_entity']
                                                 )).expandtabs(10))

    return


def is_english_sentence(astr, nlp):
    doc = nlp(astr)
    legit_pos = list(filter(lambda token: token.pos_ not in EXCL_POS, doc))

    verdict = (len(legit_pos) >= 2)     # "2" to reduce FPs such as addresses

    #print(astr, verdict)

    return verdict


def get_description_stats(report, nlp):
    global qspecs

    total_desc = 0
    engl_desc = 0
    for f in qspecs:
        qspec = qspecs[f]
        for desc_node in qspec.get_desc_objs():
            # Get the desc string
            desc_str_node = list(qspec.G.neighbors(desc_node))[0]
            desc_str = qspec.G.nodes[desc_str_node]['nodenameraw']
            total_desc += 1
            if is_english_sentence(desc_str, nlp):
                engl_desc += 1

    redo_desc = (1 - (engl_desc*1.0/total_desc))*100.0
    print('* %02d%% of descriptions need work.' % redo_desc)
    return


def most_frq_violation(filename, report):

    codes = []
    for v in report['files'][filename]['meta']:
        code_str = '[%s] %s' % (v['v_ruleid'], v['v_description'])
        codes.append(code_str)

    try:
        mfrq = sorted(Counter(codes).items(), key=operator.itemgetter(1),
                      reverse=True)[0]
    except IndexError:
        # no violations
        mfrq = ('-', 0)

    return mfrq


def write_pdf_json(report, output_json, cvrules_path):

    # Page 1 data

    # Page 1: Section 1
    report['pdf']['page1']['sec1'] = {}
    now = datetime.now()
    report['pdf']['page1']['sec1']['today'] = \
                                    datetime.strftime(now, '%a, %B %d, %Y')
    report['pdf']['page1']['sec1']['file_name'] = \
                                    report['file_name'].split('/')[-1]
    report['pdf']['page1']['sec1']['max_risk_score'] = report['max_risk']
    report['pdf']['page1']['sec1']['severity'] = \
                                    get_severity(report['max_risk'])
    report['pdf']['page1']['sec1']['num_appsvcs'] = report['num_appsvcs']
    report['pdf']['page1']['sec1']['total_apis'] = report['total_apis']

    # Page 2 data
    with open(cvrules_path) as inf:
        rules_dict = json.load(inf)
        ruleid2impact = {}
        for rule in rules_dict['rules']:
            ruleid2impact[rule['ruleid']] = rule.get('impact', None)

    report['pdf']['page2'] = {}

    sev_ctr = Counter()
    absent_impacts = set()
    for f in report['files']:
        for v in report['files'][f]['violations']:
            api = api_fn(v['v_entity']) or 'Global'
            sev = v['v_severity']
            desc = v['v_description']
            if sev not in report['pdf']['page2']:
                report['pdf']['page2'][sev] = {}
            if desc not in report['pdf']['page2'][sev]:
                report['pdf']['page2'][sev][desc] = {}
                report['pdf']['page2'][sev][desc]['Impact'] = None
                report['pdf']['page2'][sev][desc]['Count'] = []

            # Add the impact
            impact = ruleid2impact[v['v_ruleid']]
            if impact is None:
                absent_impacts.add(desc)
            report['pdf']['page2'][sev][desc]['Impact'] = impact

            # Add the formatted violation
            vstr = '%s\n\n%s' % (api, v['v_entity'])
            report['pdf']['page2'][sev][desc]['Count'].append(vstr)

            sev_ctr[sev] += 1

    # Post-process the PDF json
    for sev in ['Critical', 'High', 'Medium', 'Low']:
        if sev not in report['pdf']['page2']:
            continue

        sorted_v = sorted(report['pdf']['page2'][sev].items(),
                          key=lambda x: len(x[1]['Count']), reverse=True)
        sev_key = '%s (%d)' % (sev, sev_ctr[sev])
        report['pdf']['page2'][sev_key] = {}
        for elem in sorted_v:
            report['pdf']['page2'][sev_key][elem[0]] = {}
            report['pdf']['page2'][sev_key][elem[0]]['Impact'] = elem[1]['Impact']
            count_key = 'Count (%d)' % len(elem[1]['Count'])
            report['pdf']['page2'][sev_key][elem[0]][count_key] = elem[1]['Count']

        # Finally drop the original key
        report['pdf']['page2'].pop(sev)

    if output_json is not None:
        # Write the data structure
        with open(output_json, 'w') as outf:
            json.dump(report, outf)

    return


def write_json(report, output_json):

    # Repurpose the "report" data structure
    for f in report['files']:

        report['files'][f]['properties'] = {}
        if report['files'][f]['status'] == 'err':
            report['files'][f]['properties']['status'] = \
                                report['files'][f].pop('status')
            report['files'][f]['properties']['err_detail'] = \
                                report['files'][f].pop('meta')
            report['files'][f]['violations'] = []
        else:
            # Rename the "meta" key to "violations"
            report['files'][f]['violations'] = report['files'][f].pop('meta')
            # Bring file properties together
            report['files'][f]['properties'] = {}
            report['files'][f]['properties']['score'] = \
                                report['files'][f].pop('score')
            report['files'][f]['properties']['status'] = \
                                report['files'][f].pop('status')
            report['files'][f]['properties']['num_apis'] = \
                                report['files'][f].pop('num_apis')
            report['files'][f]['properties']['num_params'] = \
                                report['files'][f].pop('num_params')
            report['files'][f]['properties']['num_evaluations'] = \
                                report['files'][f].pop('num_evaluations')
            report['files'][f]['properties']['version'] = \
                                report['files'][f].pop('version')

            for api in report['files'][f]['apis']:
                report['files'][f]['apis'][api]['violations'] = \
                        report['files'][f]['apis'][api].pop('meta')

    if output_json is not None:
        # Write the data structure
        with open(output_json, 'w') as outf:
            json.dump(report, outf)

    return


def compare_specs(ospec, uspec, output_json, cvrules_path, rules_path=None):

    report = {}
    report['pdf'] = {}
    report['pdf']['page1'] = {}

    report['files'] = {}
    for abs_path in (ospec, uspec):
        check_one_spec(abs_path, report, cvrules_path, rules_path=rules_path)

    # Now get statistics between the two files
    print('-'*100)
    print(('\t*** Spec Comparison ***\n\n').expandtabs(40))
    print(('* File:\t%s\t%s' % (ospec, uspec)).expandtabs(40))
    print(('* Version:\t%s\t%s' % (report['files'][ospec]['version'],
                            report['files'][uspec]['version'])).expandtabs(40))

    num_violations_o = len(report['files'][ospec]['meta'])
    num_violations_u = len(report['files'][uspec]['meta'])
    print(('* Number of violations:\t%d\t%d' % (num_violations_o,
                                            num_violations_u)).expandtabs(40))

    ospec_score = report['files'][ospec]['score']
    ospec_severity = get_severity(ospec_score)
    uspec_score = report['files'][uspec]['score']
    uspec_severity = get_severity(uspec_score)
    print(('* Score:\t%d\t%d' % (ospec_score, uspec_score)).expandtabs(40))
    print(('* Severity:\t%s\t%s' % (ospec_severity,
                                    uspec_severity)).expandtabs(40))
    # Most frequent violation
    mfrq_ospec = most_frq_violation(ospec, report)
    mfrq_uspec = most_frq_violation(uspec, report)
    print(('* Most frq violation:\t%s (%d)\t%s (%d)' % \
            (mfrq_ospec[0], mfrq_ospec[1], mfrq_uspec[0], mfrq_uspec[1])).expandtabs(40))

    write_json(report, output_json)

    return


def generate_report_zip(spec_zip, output_json, cvrules_path,
                        rules_path=None):

    report, unzip_dir = check_specs(spec_zip, cvrules_path,
                                    rules_path=rules_path)

    print('='*100)
    print('\t'*3, '** Imperva API Risk Assessment Report **')
    print('\t'*3, '-'*45, '\n'*2)

    nlp = None  #spacy.load("en_core_web_sm")
    print('Initializing...')
    #return report

    print('-'*100)
    high_level_info(report)
    print('-'*100)
    analyze_apps(report)
    print('-'*100)
    analyze_apis(report)
    print('-'*100)
    common_themes(report, nlp)
    print('-'*100)
    insights(report)
    print('-'*100)
    if spec_zip.endswith('orangebank.zip'):
        spec_path = '%s/orangebank_stores.json' % unzip_dir
        #spec_path = random.sample(report['files'].keys(), 1)[0]
        print_samples(report, spec_path)

    write_json(report, output_json)
    write_pdf_json(report, output_json, cvrules_path)

    return report


def generate_report_spec(spec_path, output_json, cvrules_path,
                         rules_path=None):
    report = {}

    # Get the filename
    report['file_name'] = spec_path

    # Get the file timestamp
    report['file_modified_time'] = \
        str(datetime.fromtimestamp(int(os.path.getmtime(spec_path))))

    report['pdf'] = {}
    report['pdf']['page1'] = {}

    report['files'] = {}
    check_one_spec(spec_path, report, cvrules_path, rules_path=rules_path)

    # Check for errors
    if report['files'][spec_path]['status'] == 'err':
        return report

    print('-'*100)
    high_level_info(report)
    print('-'*100)
    analyze_apps(report)
    print('-'*100)
    analyze_apis(report)

    # Num APIs
    print(('* Number of APIs:\t%d' %
                    report['files'][spec_path]['num_apis']).expandtabs(40))
    # Num parameters
    print(('* Number of parameters:\t%d' %
                    report['files'][spec_path]['num_params']).expandtabs(40))

    # Num of violations
    total_violations = len(report['files'][spec_path]['meta'])
    total_evaluations = report['files'][spec_path]['num_evaluations']
    print(('* Number of violations:\t%d (out of %d checks)' %
                    (total_violations, total_evaluations)).expandtabs(40))

    # Score assigned
    print(('* Score:\t%d' % report['files'][spec_path]['score']).expandtabs(40))
    # Severity assigned
    severity = get_severity(report['files'][spec_path]['score'])
    print(('* Severity:\t%s' % severity).expandtabs(40))
    # All violations
    print_samples(report, spec_path)

    # Always remove PDF data
    report.pop('pdf', None)
    write_json(report, output_json)

    return report

def check_cicd_criteria(report, cicd_criteria_path):
    scores = []
    for f in report['files']:
        if report['files'][f]['properties']['status'] == 'err':
            continue
        scores.append(report['files'][f]['properties']['score'])

    with open(cicd_criteria_path) as inf:
        for line in inf:
            if line.startswith('#'):
                # Skip comments
                continue
            code, _ = line.strip().split('\t', 1)

            if code == 'CICD01':
                # Check if any file is has a CRITICAL issue
                if len(list(filter(lambda x: x >= 9, scores))) > 0:
                    print('CICD code %s triggered...' % code)
                    sys.exit(1)
            if code == 'CICD02':
                # Check if any file is has a HIGH issue
                if len(list(filter(lambda x: x >= 6, scores))) > 0:
                    print('CICD code %s triggered...' % code)
                    sys.exit(1)
            if code == 'CICD03':
                # Check if any file is has a MEDIUM issue
                if len(list(filter(lambda x: x >= 4, scores))) > 0:
                    print('CICD code %s triggered...' % code)
                    sys.exit(1)
            if code == 'CICD04':
                # Check if any file is has a LOW issue
                if len(list(filter(lambda x: x >= 1, scores))) > 0:
                    print('CICD code %s triggered...' % code)
                    sys.exit(1)
            if code == 'CICD05':
                pass

    return


def main(argv=sys.argv):
    apar = ArgumentParser()
    subpar = apar.add_subparsers(help='sub-command help', dest='command')

    parser_eval_risk = subpar.add_parser('eval_risk', help='eval_risk help')
    group = parser_eval_risk.add_mutually_exclusive_group()
    group.add_argument('-z', dest='spec_zip_path',
                                  help='Spec zip path')
    group.add_argument('-s', dest='spec_file_path',
                                  help='Spec file path')
    parser_eval_risk.add_argument('-i', dest='cv_rules_path',
                                  help='Imperva rules path')
    parser_eval_risk.add_argument('-r', dest='custom_rules_path',
                                  help='Custom rules path')
    parser_eval_risk.add_argument('-o', dest='output_json_path',
                                  required=True, help='Output JSON path')
    parser_eval_risk.add_argument('-c', dest='cicd_criteria_path',
                                  help='CICD criterion file path')
    parser_eval_risk.add_argument('-u', dest='customer_name', default='N/A',
                                  help='Customer Name (optional)')

    parser_compare = subpar.add_parser('trend_risk', help='trend_risk help')
    parser_compare.add_argument('original_spec_file_path', type=str,
                                help='Original spec file path')
    parser_compare.add_argument('updated_spec_file_path', type=str,
                                help='Updated spec file path')
    parser_compare.add_argument('-i', dest='cv_rules_path',
                                help='Imperva rules path')
    parser_compare.add_argument('-r', dest='custom_rules_path',
                                help='Custom rules path')
    parser_compare.add_argument('-o', dest='output_json_path',
                                required=True, help='Output JSON path')
    parser_compare.add_argument('-u', dest='customer_name', default='N/A',
                                help='Customer Name (optional)')

    args = apar.parse_args(argv[1:])

    if not (args.cv_rules_path or args.custom_rules_path):
        print('Error: Specify path to either the Imperva rules or custom'
              ' rules')
        return

    if args.command == 'trend_risk':
        compare_specs(args.original_spec_file_path, args.updated_spec_file_path,
                      args.output_json_path, args.cv_rules_path,
                      args.custom_rules_path)
    elif args.command == 'eval_risk':

        if args.cicd_criteria_path:
            # Disable stdout
            sys.stdout = open(os.devnull, 'w')

        if args.spec_zip_path:
            report = generate_report_zip(args.spec_zip_path,
                                         args.output_json_path,
                                         args.cv_rules_path,
                                         args.custom_rules_path)
            # generate_html(report, args.output_json_path)
            generate_html_new(report, args.output_json_path, args.customer_name)

        if args.spec_file_path:
            report = generate_report_spec(args.spec_file_path,
                                          args.output_json_path,
                                          args.cv_rules_path,
                                          args.custom_rules_path)
        if args.cicd_criteria_path:
            check_cicd_criteria(report, args.cicd_criteria_path)

    return

def compute_counts(report):
    """
    {
        'num_of_params': 12,
        'num_of_data_types': 1,
        'response_codes': [
            '200',
            'default'
        ],
        'response_codes_count': [
            5,
            5
        ],
        'd_types': [
            'list'
        ],
        'd_type_counts': [
            4
        ],
        'req_method_list': ['GET', 'POST'],
        'req_method_count': [20, 10],
        'num_evaluations': 443
    }
    """

    counts = {
        'num_of_params': 0,
        'num_of_data_types': 0,
        'response_codes': [],
        'response_codes_count': [],
        'd_types': [],
        'd_type_counts': [],
        'req_method_list': [],
        'req_method_count': [],
        'num_evaluations': 0,
    }
    res_codes = {}
    d_types = {}
    request_methods = {}
    files = report.get('files')
    for key, value in files.items():
        if value.get('properties', {}).get('status') == 'err':
            continue
        counts['num_evaluations'] += value.get('properties', {}).get('num_evaluations', 0)
        counts['num_of_params'] += value.get('properties', {}).get('num_params', 0)
        counts['num_of_data_types'] += len(value.get('data_types'))

        req_methods = value.get('req_method', {})
        for method, req_count in req_methods.items():
            if method in request_methods:
                request_methods[method] += req_count
            else:
                request_methods[method] = req_count

        response_codes = value.get('response_codes', {})
        for res_code, r_count in response_codes.items():
            if res_code in res_codes:
                res_codes[res_code] += r_count
            else:
                res_codes[res_code] = r_count

        data_types = value.get('data_types', {})
        for d_type, count in data_types.items():
            if d_type in d_types:
                d_types[d_type] += count
            else:
                d_types[d_type] = count

    r_codes, r_counts = [], []
    for r_code, r_count in res_codes.items():
        r_codes.append(r_code)
        r_counts.append(r_count)
    counts['response_codes'] = r_codes
    counts['response_codes_count'] = r_counts

    dt_types, dt_counts = [], []
    for d_type, d_count in d_types.items():
        dt_types.append(d_type)
        dt_counts.append(d_count)
    counts['d_types'] = dt_types
    counts['d_type_counts'] = dt_counts

    req_method_list, req_method_count = [], []
    for req_method, req_count in request_methods.items():
        req_method_list.append(req_method.upper())
        req_method_count.append(req_count)
    counts['req_method_list'] = req_method_list
    counts['req_method_count'] = req_method_count

    return counts

def contains_param(entity):
    if entity.startswith('(#->paths') and "parameters->" in entity:
        return True
    return False

def get_highest_sev_params_api_count(report, sev, ctg):
    param_list = set()
    api_list = set()
    files = report.get('files', {})
    for file_name, val in files.items():
        apis = val.get('apis', {})
        for api, api_val in apis.items():
            violations = api_val.get('violations', [])
            for violation in violations:
                entity = violation.get('v_entity', '')
                if violation.get('v_severity', '') == sev and violation.get('v_risk_ctg', '') == ctg:
                    if contains_param(entity): 
                        param_list.add(get_param_from_entity(entity))
                    api_list.add(api)
    return len(param_list), len(api_list)


def compute_violation_counts(report):
    """
    {
        'most_occ_cat_count': 2,
        'most_occ_cat': 'Undefined Bounds',
        'description': 'properties of type "array" should have "maxItems" defined.',
        'API Lifecycle & Management': {
            'risk_sub_ctg': {
                'Missing information': 1
            },
            'total_count': 1,
            'highest_sev': 'Low',
            'Low': 1,
            'highest_sev_count': 1
        },
        'Data Type Definitions': {
            'risk_sub_ctg': {
            'Undefined Bounds': 2
            },
            'total_count': 2,
            'highest_sev': 'High',
            'High': 2,
            'highest_sev_count': 2
        },
        'risk_siv_counts': {
            'critical': 0,
            'high': 2,
            'medium': 0,
            'low': 1
        }
    }
    """
    violation_counts = {}
    risk_siv_counts = {
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0,
    }
    for key, value in report.get('files', {}).items():
        violations = value.get('violations', [])
        for each_violation in violations:
            severity = each_violation.get('v_severity')
            risk_ctg = each_violation.get('v_risk_ctg')
            risk_sub_ctg = each_violation.get('v_risk_subctg')
            description = each_violation.get('v_description')
            entity = each_violation.get('v_entity')
            risk_ctg_counts = {
                'risk_sub_ctg': {}
            }
            risk_siv_counts[severity.lower()] += 1

            highest_sev = None
            if risk_ctg in violation_counts:
                risk_ctg_counts = violation_counts[risk_ctg]

                if risk_sub_ctg in risk_ctg_counts.get('risk_sub_ctg', {}):
                    risk_ctg_counts['risk_sub_ctg'][risk_sub_ctg] += 1
                else: 
                    risk_ctg_counts['risk_sub_ctg'][risk_sub_ctg] = 1

                if severity in risk_ctg_counts:
                    risk_ctg_counts[severity] += 1
                else:
                    risk_ctg_counts[severity] = 1

                if 'total_count' in risk_ctg_counts:
                    risk_ctg_counts['total_count'] += 1
                else: 
                    risk_ctg_counts['total_count'] = 1

                if 'highest_sev' in risk_ctg_counts:
                    highest_sev = risk_ctg_counts['highest_sev']
                    if highest_sev.lower() == 'critical':
                        continue
                    elif highest_sev.lower() == 'high' and severity.lower() == 'critical':
                        highest_sev = severity
                    elif highest_sev.lower() == 'medium' and severity.lower() in ['critical', 'high']:
                        highest_sev = severity
                    elif highest_sev.lower() == 'low' and severity.lower() in ['critical', 'high', 'medium']:
                        highest_sev = severity
                    risk_ctg_counts['highest_sev'] = highest_sev
                else:
                    risk_ctg_counts['highest_sev'] = severity
            else:
                highest_sev = severity
                risk_ctg_counts['total_count'] = 1
                risk_ctg_counts['highest_sev'] = severity
                risk_ctg_counts[severity] = 1
                risk_ctg_counts['risk_sub_ctg'][risk_sub_ctg] = 1

            most_occ_cat = violation_counts.get('most_occ_cat', '')
            most_occ_cat_count = violation_counts.get('most_occ_cat_count', 0)
            if risk_ctg_counts['risk_sub_ctg'][risk_sub_ctg] > most_occ_cat_count:
                violation_counts['most_occ_cat_count'] = risk_ctg_counts['risk_sub_ctg'][risk_sub_ctg]
                violation_counts['most_occ_cat'] = risk_sub_ctg
                violation_counts['description'] = description

            violation_counts[risk_ctg] = risk_ctg_counts

    violation_counts['risk_siv_counts'] = risk_siv_counts
    for k, v in violation_counts.items():
        if not isinstance(violation_counts[k], dict): continue
        if 'highest_sev' not in violation_counts[k]:
            continue
        sev = violation_counts[k]['highest_sev']
        param_count, api_count = get_highest_sev_params_api_count(report, sev, k)
        violation_counts[k]['highest_sev_param_count'] = param_count
        violation_counts[k]['highest_sev_api_count'] = api_count
        violation_counts[k]['highest_sev_count'] = violation_counts[k][sev]
    return violation_counts

def get_param_from_entity(entity):
    param = ''
    start = entity.index('(') + len('(')
    end = entity.index(')', start)
    api_param = entity[start:end]
    split_list = api_param.split('->')
    for i in range(6):
        param = param + '->' + split_list[i]
    return param

def initialise_issue_insights(issue_insights, risk_ctg, risk_sub_ctg, i_type):
    issue_insights[risk_ctg][risk_sub_ctg][i_type] = set()
    issue_insights[risk_ctg][risk_sub_ctg]['critical_'+i_type] = set()
    issue_insights[risk_ctg][risk_sub_ctg]['high_'+i_type] = set()
    issue_insights[risk_ctg][risk_sub_ctg]['medium_'+i_type] = set()
    issue_insights[risk_ctg][risk_sub_ctg]['low_'+i_type] = set()

def add_sev_issue_insights(issue_insights, risk_ctg, risk_sub_ctg, i_type, val, severity):
    if not val: return
    issue_insights[risk_ctg][risk_sub_ctg][i_type].add(val)
    if severity == 'critical':
        issue_insights[risk_ctg][risk_sub_ctg]['critical_'+i_type].add(val)
    elif severity == 'high':
        issue_insights[risk_ctg][risk_sub_ctg]['high_'+i_type].add(val)
    elif severity == 'medium':
        issue_insights[risk_ctg][risk_sub_ctg]['medium_'+i_type].add(val)
    else:
        issue_insights[risk_ctg][risk_sub_ctg]['low_'+i_type].add(val)

def add_violation(issue_insights, violation, file_name, api=''):
    violation_hash = hashlib.md5((json.dumps(violation) + file_name).encode()).hexdigest()
    if violation_hash in issue_insights.get('hash_list', set()):
        return
    risk_ctg = violation.get('v_risk_ctg', '')
    risk_sub_ctg = violation.get('v_risk_subctg', '')
    severity = violation.get('v_severity', '').lower()
    entity = violation.get('v_entity', '')
    tags = violation.get('v_tags', '')
    if risk_ctg not in issue_insights:
        issue_insights[risk_ctg] = {}
    if risk_sub_ctg not in issue_insights[risk_ctg]:
        issue_insights[risk_ctg][risk_sub_ctg] = {}
    if 'apis' not in issue_insights[risk_ctg][risk_sub_ctg]:
        initialise_issue_insights(issue_insights, risk_ctg, risk_sub_ctg, 'apis')
    if 'files' not in issue_insights[risk_ctg][risk_sub_ctg]:
        initialise_issue_insights(issue_insights, risk_ctg, risk_sub_ctg, 'files')
    if 'params' not in issue_insights[risk_ctg][risk_sub_ctg]:
        initialise_issue_insights(issue_insights, risk_ctg, risk_sub_ctg, 'params')
    if 'tags' not in issue_insights[risk_ctg][risk_sub_ctg]:
        issue_insights[risk_ctg][risk_sub_ctg]['tags'] = set()
    if severity not in issue_insights[risk_ctg][risk_sub_ctg]:
        issue_insights[risk_ctg][risk_sub_ctg][severity] = 0
    if 'hash_list' not in issue_insights:
        issue_insights['hash_list'] = set()
    if 'param_list' not in issue_insights[risk_ctg]:
        issue_insights[risk_ctg]['param_list'] = set()
    if 'api_list' not in issue_insights[risk_ctg]:
        issue_insights[risk_ctg]['api_list'] = set()
    if 'file_list' not in issue_insights[risk_ctg]:
        issue_insights[risk_ctg]['file_list'] = set()
    issue_insights[risk_ctg][risk_sub_ctg][severity] += 1
    issue_insights['hash_list'].add(violation_hash)
    issue_insights[risk_ctg]['file_list'].add(file_name)
    for tag in tags:
        issue_insights[risk_ctg][risk_sub_ctg]['tags'].add(tag)
    add_sev_issue_insights(issue_insights, risk_ctg, risk_sub_ctg, 'files', file_name, severity)
    if api != '':
        issue_insights[risk_ctg]['api_list'].add(api)
        add_sev_issue_insights(issue_insights, risk_ctg, risk_sub_ctg, 'apis', api, severity)
    if contains_param(entity):
        param = get_param_from_entity(entity)
        issue_insights[risk_ctg]['param_list'].add(param)
        add_sev_issue_insights(issue_insights, risk_ctg, risk_sub_ctg, 'params', param, severity)

def get_issue_insights(report):
    """
    {
        'Data Type Definitions': {
            'Undefined Bounds': {
                'apis': {
                    'orangebank_user.json:/history'
                },
                'files': {
                    'cvapirisk_pkg/orangebank_user.json'
                },
                'high': 1
            }
        }
    }
    """
    issue_insights = {}
    files = report.get('files', {})
    for file_name, record in files.items():
        apis = record.get('apis', {})
        for api, val in apis.items():
            violations = val.get('violations', [])
            for each_violation in violations:
                add_violation(issue_insights, each_violation, file_name, api)
        violations = record.get('violations', [])
        for violation in violations:
            add_violation(issue_insights, violation, file_name)
    return issue_insights

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        try:
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
        except FileExistsError:
            pass

def generate_html_new(report, output_path, customer_name='N/A'):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(curr_dir, 'sparc-templates-new')
    output_dir = os.path.join(os.path.dirname(os.path.abspath(output_path)), 'sparc_report')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Copy css files to output directory
    copytree(templates_dir, output_dir, symlinks = True)
    os.remove(os.path.join(output_dir, 'risk-report-template-generic.html'))

    # NOTE: I have deleted index_raw.html from the template folder but for
    # some reason this file is still present on pypi server.
    # TODO: delete next 3 lines when index_raw.html is removed from pypi package
    index_raw = os.path.join(output_dir, 'index_raw.html')
    if os.path.isfile(index_raw):
        os.remove(index_raw)

    html_file = os.path.join(output_dir, 'index.html')
    current_time = datetime.now()
    dt_string = current_time.strftime("%B %d, %Y %H:%M:%S")

    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('risk-report-template-generic.html')

    counts = compute_counts(report)
    violation_counts = compute_violation_counts(report)
    issue_insights = get_issue_insights(report)
    violation_details_old = report.get('pdf', {}).get('page2', {})

    violation_details = {'Critical': {}, 'Major': {}, 'Minor': {}}
    for key, value in violation_details_old.items():
        if 'critical' in key.lower() or 'high' in key.lower():
            violation_details['Critical'].update(value)
        elif 'medium' in key.lower():
            violation_details['Major'].update(value)
        elif 'low' in key.lower():
            violation_details['Minor'].update(value)

    with open(html_file, 'w') as fh:
        fh.write(template.render(
            customer_name = customer_name,
            created_time = dt_string,
            file_name = report.get('file_name', 'N/A'),
            num_of_files = len(report.get('files')),
            num_of_apis = report.get('total_apis', 0),
            num_of_params = counts.get('num_of_params', 0),
            num_of_data_types = counts.get('num_of_data_types', 0),
            response_codes = counts.get('response_codes', []),
            r_codes_count = counts.get('response_codes_count', []),
            data_types = counts.get('d_types', []),
            data_type_counts = counts.get('d_type_counts', []),
            req_method_list = counts.get('req_method_list', []),
            req_method_count = counts.get('req_method_count', []),
            violations = violation_counts,
            num_of_evaluations = counts.get('num_evaluations', 0),
            issue_insights = issue_insights,
            violation_details = violation_details,
        ))
    return


def generate_html(report, output_path):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(curr_dir, 'sparc-templates')
    output_dir = os.path.join(os.path.dirname(os.path.abspath(output_path)), 'sparc_report_old')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #Copy css files to output directory
    copytree(templates_dir, output_dir, symlinks = True)

    html_file = os.path.join(output_dir, 'index.html')

    current_time = datetime.now()
    dt_string = current_time.strftime("%B %d, %Y %H:%M:%S")

    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('risk-report-template-generic.html')

    counts = compute_counts(report)
    violation_counts = compute_violation_counts(report)
    issue_insights = get_issue_insights(report)
    violation_details = report.get('pdf', {}).get('page2', {})

    with open(html_file, 'w') as fh:
        fh.write(template.render(
            created_time = dt_string,
            num_of_files = len(report.get('files')),
            num_of_apis = report.get('total_apis', 0),
            num_of_params = counts.get('num_of_params', 0),
            num_of_data_types = counts.get('num_of_data_types', 0),
            response_codes = counts.get('response_codes', []),
            r_codes_count = counts.get('response_codes_count', []),
            data_types = counts.get('d_types', []),
            data_type_counts = counts.get('d_type_counts', []),
            req_method_list = counts.get('req_method_list', []),
            req_method_count = counts.get('req_method_count', []),
            violations = violation_counts,
            num_of_evaluations = counts.get('num_evaluations', 0),
            issue_insights = issue_insights,
            violation_details = violation_details,
        ))
    return

if __name__ == '__main__':
    sys.exit(main())
