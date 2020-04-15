def ssv_splitter(ssv):
    """
    Given a string containing space separated values, it returns a list of values. First and last element are removed.
    :param ssv: space separated values
    :return: list of values
    """

    strings = ssv.split()
    strings.pop()
    strings.pop(0)
    return strings


def CA_builder(ca_rule):
    """
    Given a string containing a CAN_ASSIGN rule, it returns a tuple built from it.
    :param ca_rule: CAN_ASSIGN rule string
    :return: tuple containing:  - administrative role
                                - immutable set of positive pre-conditions
                                - immutable set of negative pre-conditions
                                - target role
    """
    pre_conditions = ca_rule[1].split('&')
    positives = set()
    negatives = set()
    for condition in pre_conditions:
        if condition.startswith('-'):
            tmp = condition[1:]
            negatives.add(tmp)
        else:
            if condition != 'TRUE':
                positives.add(condition)
    positives = frozenset(positives)
    negatives = frozenset(negatives)
    new_ca_rule = (ca_rule[0], positives, negatives, ca_rule[2])
    return new_ca_rule


def list_to_set(list_of_strings, ca_rules=0):
    """
    Given a list of strings it returns a set of tuples built from it.
    From every string, starting and ending characters (<, >) are removed, then is built a tuple. If strings contain
    CA_RULES, then is called CA_builder.
    :param list_of_strings: list of strings, each of them in following format: <STRING>
    :param ca_rules: flag needed to build CA_RULES
    :return: set of tuples
    """
    tuples = set()
    for string in list_of_strings:
        truncated = string[1:-1]
        truncated = truncated.split(',')
        if ca_rules:
            truncated = CA_builder(truncated)
        my_tuple = tuple(truncated)
        tuples.add(my_tuple)
    return tuples


class Parser:
    """
    Object that can open a .arbac file and parse the specification of a role reachability problem.
    """
    def __init__(self):
        """
        Simple constructor which initializes data structures.
         """
        self.roles = set()
        self.users = set()
        self.user_to_role = set()
        self.can_remove = set()
        self.can_assign = set()
        self.goal = set()

    def open_file(self, i):
        """
        Opens the i-th policy file contained in the policies folder and parses it.
        Knowing the file format, every line can be distinguished by an identifiable word.
        :param i: i-th arbac policy to inspect
        :return: None
        """

        filename = 'policies/policy' + str(i) + '.arbac'
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith("Roles"):
                    self.roles = set(ssv_splitter(line))
                if line.startswith("Users"):
                    self.users = ssv_splitter(line)
                if line.startswith("UA"):
                    self.user_to_role = list_to_set(ssv_splitter(line))
                if line.startswith("CR"):
                    self.can_remove = list_to_set(ssv_splitter(line))
                if line.startswith("CA"):
                    self.can_assign = list_to_set(ssv_splitter(line), 1)
                if line.startswith("Goal"):
                    self.goal = ssv_splitter(line).pop()
        return None

    def get_roles(self):
        """
        Returns the ROLES set of the role reachability problem
        :return: ROLES set
        """
        return self.roles

    def get_users(self):
        """
        Returns the USERS set of the role reachability problem
        :return: USERS set
        """
        return self.users

    def get_user_to_role(self):
        """
        Returns the USER_TO_ROLE set of the role reachability problem
        :return: USER_TO_ROLE set
        """
        return self.user_to_role

    def get_can_remove(self):
        """
        Returns the CAN_REMOVE set of rules of the role reachability problem
        :return: CAN_REMOVE set
        """
        return self.can_remove

    def get_can_assign(self):
        """
        Returns the CAN_ASSIGN set of rules of the role reachability problem
        :return: CAN_ASSIGN set
        """
        return self.can_assign

    def get_goal(self):
        """
        Return the GOAL of the role reachability problem
        :return: GOAL
        """
        return self.goal
