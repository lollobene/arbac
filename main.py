import parser
import arbac

"""
Main of the project.
First from a parser is imported the policy which needs to be analyzed and created the ARBAC.
Then is performed the backward slicing.
Finally is solved the role reachability problem.
"""
if __name__ == '__main__':
    for i in range(1, 9):
        parser = parser.Parser()
        parser.open_file(i)
        my_policy = arbac.Arbac(
            parser.get_roles(),
            parser.get_users(),
            parser.get_user_to_role(),
            parser.get_can_remove(),
            parser.get_can_assign(),
            parser.get_goal()
        )

        my_policy.backward_slicing()
        result = my_policy.role_reachability()
        print(result)




