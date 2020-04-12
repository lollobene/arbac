import itertools
import pruning


class Arbac:

    def __init__(self, roles, users, user_to_role, can_remove, can_assign, goal):
        self.roles = roles
        self.users = users
        self.user_to_role = user_to_role
        self.can_remove = can_remove
        self.can_assign = can_assign
        self.goal = goal

    def backward_slicing(self):
        prng = pruning.Pruning(self.roles, self.can_remove, self.can_assign, self.goal)
        prng.backward_slicing()
        self.can_assign = prng.get_can_assign()
        self.can_remove = prng.get_can_remove()
        self.roles = prng.get_roles()

    def role_reachability(self):
        permutations = list(itertools.permutations(self.can_assign))
        for permutation in permutations:
            checkpoint = set(self.user_to_role)
            for ca_rule in permutation:
                for user in self.users:
                    # print(ca_rule)
                    self.apply_ca_rule(user, ca_rule)

            if self.check_target():
                # print('Broke!!!!!!!!!!!!!!!!!!')
                return 1
            else:
                self.user_to_role = set(checkpoint)

            # print('User to role: ')
            # print(user_to_role)

        return 0

    def apply_ca_rule(self, user, ca_rule):
        # print(ca_rule)
        if not self.check_administrative_role(ca_rule):
            return False
        roles = self.user_roles(user)
        # print(roles)
        for role in roles:
            if role == ca_rule[3]:
                # print('Already a ' + role)
                return False
        for positive_role in ca_rule[1]:
            if not positive_role in roles:
                return False

        for negative_role in ca_rule[2]:
            if negative_role in roles:
                return False
        self.add_utl(user, ca_rule[3])
        return True

    def check_administrative_role(self, ca_rule):
        # check whether if the administrative role exists in the user-to-role set
        for pair in self.user_to_role:
            if pair[1] == ca_rule[0]:
                return True
        return False

    def user_roles(self, user):
        tmp = []
        for ur in self.user_to_role:
            if ur[0] == user:
                tmp.append(ur[1])
        return tmp

    def add_utl(self, user, role):
        pair = (user, role)
        self.user_to_role.add(pair)

    def check_target(self):
        for utr in self.user_to_role:
            if utr[1] == 'target':
                return 1
        return 0

    def print_all(self):
        print('Roles: ')
        print(self.roles)
        print('Users: ')
        print(self.users)
        print('User to role: ')
        print(self.user_to_role)
        print('Can remove rules: ')
        print(self.can_remove)
        print('Can assign rules: ')
        print(self.can_assign)
        print('Goal: ')
        print(self.goal)
