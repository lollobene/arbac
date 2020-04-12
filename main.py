import arbac_parser
import arbac

if __name__ == '__main__':

    for i in range(1, 9):
        parser = arbac_parser.Parser()
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
        flag = my_policy.role_reachability()
        print(flag)




