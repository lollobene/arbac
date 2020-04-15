import itertools
import pruning


class Arbac:
    """
    Object that can perform classical actions of Administrative RBAC policy.
    """

    def __init__(self, roles, users, user_to_role, can_remove, can_assign, goal):
        """
        Constructor of the class that initializes data structures.
        :param roles: set of roles
        :param users: set of users
        :param user_to_role: set of user_to_role pairs
        :param can_remove: set of can_remove rules
        :param can_assign: set of can assign rules
        :param goal: goal role
        """
        self.roles = roles
        self.users = users
        self.user_to_role = user_to_role
        self.can_remove = can_remove
        self.can_assign = can_assign
        self.goal = goal

    def backward_slicing(self):
        """
        Pruning algorithm that performs backward_slicing.
        Roles, can_assign and can_remove sets are modified.
        Main operations are delegated to Pruning object.
        :return: None
        """
        prng = pruning.Pruning(self.roles, self.can_remove, self.can_assign, self.goal)
        prng.backward_slicing()
        self.can_assign = prng.get_can_assign()
        self.can_remove = prng.get_can_remove()
        self.roles = prng.get_roles()
        return None

    def role_reachability(self):
        """
        Main operation to solve the role reachability problem. First all permutations of the can_assign set are
        calculated. Then, for every permutation, all ca_rules are applied. Finally checks if target role has been
        assigned to some user.
        :return: 1 if the target role has been assigned, 0 otherwise.
        """
        permutations = list(itertools.permutations(self.can_assign))
        for permutation in permutations:
            checkpoint = set(self.user_to_role)
            for ca_rule in permutation:
                for user in self.users:
                    self.apply_ca_rule(user, ca_rule)
            if self.check_target():
                return 1
            else:
                self.user_to_role = set(checkpoint)
        return 0

    def apply_ca_rule(self, user, ca_rule):
        """
        Given a user and a ca_rule, this function tries to apply the rule by assigning the target role to the user.
        First checks if the administrative role exists and if the user already owns target role.
        Then all positive and negative preconditions are checked.
        Finally target role is assigned.
        :param user: user
        :param ca_rule: can_assign rule
        :return: True if the target role can be assigned to the user, False otherwise.
        """
        if not self.check_administrative_role(ca_rule):
            return False
        roles = self.get_user_roles(user)
        for role in roles:
            if role == ca_rule[3]:
                return False
        for positive_role in ca_rule[1]:
            if positive_role not in roles:
                return False
        for negative_role in ca_rule[2]:
            if negative_role in roles:
                return False
        self.add_utl(user, ca_rule[3])
        return True

    def check_administrative_role(self, ca_rule):
        """
        Given a can_assign rule, this function checks if the administrative role exists in user_to_role set.
        :param ca_rule: can_assign rule
        :return: True if rule can be applied, False otherwise
        """
        for pair in self.user_to_role:
            if pair[1] == ca_rule[0]:
                return True
        return False

    def get_user_roles(self, user):
        """
        Given a user, all roles assigned to the user are returned.
        :param user: user
        :return: list of roles
        """
        roles = []
        for ur in self.user_to_role:
            if ur[0] == user:
                roles.append(ur[1])
        return roles

    def add_utl(self, user, role):
        """
        Given a user and a role, a pair is created from them and then added to the user_to_role set.
        :param user: user
        :param role: role
        :return: NONE
        """
        pair = (user, role)
        self.user_to_role.add(pair)
        return None

    def check_target(self):
        """
        This function checks if the GOAL role has been assigned.
        :return: True if the GOAL role has been assigned, False otherwise
        """
        for utr in self.user_to_role:
            if utr[1] == 'target':
                return True
        return False

    def print_all(self):
        """
        Debugging function that prints the ARBAC state.
        :return:
        """
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
