from cvsvc_apirisk.score.base import ScoreNode, check_remed


class SpecSecSecurityAttr05(ScoreNode):

    def __init__(self, qspec, target_obj=None, attr_wt=9):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        super().__init__()

        self.fix_template = \
            '[CVSPS005] [%s]: Security field is not defined globally or '\
            'for operation object.'

        self.qspec = qspec
        self.target_obj = target_obj
        self.attr_wt = attr_wt

        return

    def __repr__(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        return 'sps-sec-attr05'

    def compute_openapiv2(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        score = 0
        remed_clues = []

        global_security_node = '%s -> security' % self.qspec.ROOT_NODE
        if not self.qspec.G.has_node(global_security_node):
            for op_node in self.qspec.get_op_objs():
                security_node = '%s -> security' % op_node
                if not self.qspec.G.has_node(security_node):
                    score = 1
                    remed_clues.append(self.fix_template % op_node)

        self.score = self.attr_wt*score
        if self.score > 0:
            self.remed_clue = remed_clues
            self.meta = [(self.attr_wt, x) for x in remed_clues]

        return

    @check_remed
    def compute(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        self.compute_openapiv2()
        return
