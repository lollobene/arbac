import copy


class Pruning:

    def __init__(self, roles, can_remove, can_assign, goal):
        self.roles = roles
        self.can_remove = can_remove
        self.can_assign = can_assign
        self.goal = goal

    def backward_slicing(self):
        s = set()
        s.add(self.goal)

        while self.backward_aux(s):
            pass
        useless_roles = self.roles.difference(s)
        # print('Useless roles :')
        # print(useless_roles)
        self.remove_ca_rules(useless_roles)
        self.remove_cr_rules(useless_roles)
        self.roles = s

    def backward_aux(self, set_of_roles):
        new_roles = copy.copy(set_of_roles)
        for role in set_of_roles:
            ca_rules = self.get_target_ca_rules(role)
            for ca_rule in ca_rules:
                # retrieving administrative role and pre-requisite roles
                ca_rule_roles = self.rule_roles(ca_rule)
                new_roles.update(ca_rule_roles)

        flag = bool(new_roles.difference(set_of_roles))
        if flag:
            set_of_roles.update(new_roles)
        return flag

    def remove_ca_rules(self, useless_roles):
        to_be_removed = set()
        for role in useless_roles:
            for ca_rule in self.can_assign:
                if ca_rule[3] == role:
                    to_be_removed.add(ca_rule)
        self.can_assign = self.can_assign.difference(to_be_removed)

    def remove_cr_rules(self, useless_roles):
        to_be_removed = set()
        for role in useless_roles:
            for cr_rule in self.can_remove:
                if cr_rule[1] == role:
                    to_be_removed.add(cr_rule)
        self.can_remove = self.can_remove.difference(to_be_removed)

    def get_target_ca_rules(self, target_role):
        rules = []
        for ca_rule in self.can_assign:
            if ca_rule[3] == target_role:
                rules.append(ca_rule)
        return rules

    @staticmethod
    def rule_roles(ca_rule):
        roles = [ca_rule[0]]
        roles = roles + list(ca_rule[1].union(ca_rule[2]))
        return roles

    def get_roles(self):
        return self.roles

    def get_can_remove(self):
        return self.can_remove

    def get_can_assign(self):
        return self.can_assign

    def get_goal(self):
        return self.goal
