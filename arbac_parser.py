def line_splitter(long_string):
    string = long_string.split()
    string.pop()
    string.pop(0)
    return string


def CA_rule_maker(ca_rule):
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
    pre_conditions = (ca_rule[0], positives, negatives, ca_rule[2])
    return pre_conditions


def list_to_set(list_of_strings, triples=0):
    tmp = set()
    for string in list_of_strings:
        truncated = string[1:-1]
        truncated = truncated.split(',')
        if triples:
            truncated = CA_rule_maker(truncated)
        my_tuple = tuple(truncated)
        tmp.add(my_tuple)
    return tmp


class Parser:

    def __init__(self):
        self.roles = set()
        self.users = set()
        self.user_to_role = set()
        self.can_remove = set()
        self.can_assign = set()
        self.goal = set()

    def open_file(self, i):
        filename = 'policies/policy' + str(i) + '.arbac'
        with open(filename, 'r') as f:
            # simple reading line-by-line
            for line in f:
                if line.startswith("Roles"):
                    self.roles = set(line_splitter(line))
                if line.startswith("Users"):
                    self.users = line_splitter(line)
                if line.startswith("UA"):
                    self.user_to_role = list_to_set(line_splitter(line))
                if line.startswith("CR"):
                    self.can_remove = list_to_set(line_splitter(line))
                if line.startswith("CA"):
                    self.can_assign = list_to_set(line_splitter(line), 1)
                if line.startswith("Goal"):
                    self.goal = line_splitter(line).pop()

    def get_roles(self):
        return self.roles

    def get_users(self):
        return self.users

    def get_user_to_role(self):
        return self.user_to_role

    def get_can_remove(self):
        return self.can_remove

    def get_can_assign(self):
        return self.can_assign

    def get_goal(self):
        return self.goal
