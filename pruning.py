import copy


class Pruning:
    """
    Object that applies pruning algorithm to the ARBAC policy.
    Backward slicing is the only algorithm implemented.
    """

    def __init__(self, roles, can_remove, can_assign, goal):
        """
        Simple constructor which initializes data structures.
         """
        self.roles = roles
        self.can_remove = can_remove
        self.can_assign = can_assign
        self.goal = goal

    def backward_slicing(self):
        """
        Core function of the pruning algorithm.
        Starting from the goal role, the set S of what we can call "needed" roles is built. The creation of S set is
        performed by an auxiliary function.
        Then "useless" roles set is created by performing a set difference operation between roles and S.
        Finally are removed useless rules from CA and CR and useless roles.
        :return: None
        """
        s = set()
        s.add(self.goal)
        while self.backward_aux(s):
            pass
        useless_roles = self.roles.difference(s)
        self.remove_ca_rules(useless_roles)
        self.remove_cr_rules(useless_roles)
        self.roles = s

    def backward_aux(self, set_of_roles):
        """
        Given a set of roles S, for each role r in S, all the roles related to a CA rule that can assign r are
        added to S.
        First, for each role r in S, we retrieve every CA_rule that assign r.
        Then for every CA_rule, we add to S the administrative role, pre-condition roles and target role if they are not
        already in S. Thanks to the set data structure, duplicates are avoided.
        :param set_of_roles: set of roles
        :return: True if new role(s) are added to S, False otherwise
        """
        new_roles = copy.copy(set_of_roles)
        for role in set_of_roles:
            ca_rules = self.get_target_ca_rules(role)
            for ca_rule in ca_rules:
                ca_rule_roles = self.rule_roles(ca_rule)
                new_roles.update(ca_rule_roles)

        flag = bool(new_roles.difference(set_of_roles))
        if flag:
            set_of_roles.update(new_roles)
        return flag

    def remove_ca_rules(self, useless_roles):
        """
        Given a set of useless_roles, all CA rules that can assign them are removed from can_assign set.
        :param useless_roles: set of roles
        :return: None
        """
        to_be_removed = set()
        for role in useless_roles:
            for ca_rule in self.can_assign:
                if ca_rule[3] == role:
                    to_be_removed.add(ca_rule)
        self.can_assign = self.can_assign.difference(to_be_removed)

    def remove_cr_rules(self, useless_roles):
        """
        Given a set of useless_roles, all CR rules that can remove them are removed from can_remove set.
        :param useless_roles:
        :return: None
        """
        to_be_removed = set()
        for role in useless_roles:
            for cr_rule in self.can_remove:
                if cr_rule[1] == role:
                    to_be_removed.add(cr_rule)
        self.can_remove = self.can_remove.difference(to_be_removed)

    def get_target_ca_rules(self, target_role):
        """
        Given a target role, all ca_rules (can be one) that can assign it are returned.
        :param target_role: role
        :return: set of role
        """
        rules = []
        for ca_rule in self.can_assign:
            if ca_rule[3] == target_role:
                rules.append(ca_rule)
        return rules

    @staticmethod
    def rule_roles(ca_rule):
        """
        Given a CA rule, all roles involved in the rule are returned.
        Role returned are:
            - administrative rule
            - pre_condition positive roles
            - pre_condition negative roles
            - target role
        :param ca_rule: rule
        :return: list of roles
        """
        roles = [ca_rule[0]]
        roles = roles + list(ca_rule[1].union(ca_rule[2]))
        return roles

    def get_roles(self):
        """
        Returns the set of roles.
        :return: set of roles
        """
        return self.roles

    def get_can_remove(self):
        """
        Returns the set of CR rules.
        :return: set of rules
        """
        return self.can_remove

    def get_can_assign(self):
        """
        Returns the set of CA rules.
        :return: set of rules
        """
        return self.can_assign

    def get_goal(self):
        """
        Returns the goal.
        :return: role
        """
        return self.goal
