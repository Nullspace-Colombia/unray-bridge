"""
    Manage 
    ---
    Set of utilites for managing the environments, documents and information 
    of the unray-bridge.

    Docs
    ---
    create-env: In order to create new custom environment this command 
    automatically creates the file that will define the training environment. 
    

"""
import argparse, shutil

def cli():

    parser = argparse.ArgumentParser(
                        prog='unray',
                        description='Helps with general tasks for the tool',
                        epilog='Made <3 by Nullspace')
    
    subparser = parser.add_subparsers()
    init = subparser.add_parser("init", help="init new environment for unray_bridge")
    env = subparser.add_parser("env", help="environments tools")
    config = subparser.add_parser("config", help= "overall configuration tools")
    
    
    
    

    # Subparsers 
    # init = init_subparser.add_subparsers("init", help="create info", description= "BE AWESOME")
    # env = init_subparser.add_subparsers("env", help="create info", description= "BE AWESOME")
    # init_subparser.add_subparsers("add-agent", help="create info", description= "BE AWESOME")
    # init_subparser.add_subparsers("obs-order", help="create info", description= "BE AWESOME")
    # init_subparser.add_subparsers("edit", help="create info", description= "BE AWESOME")
    # init_subparser.add_subparsers("run", help="create info", description= "BE AWESOME")
    # init_subparser.add_subparsers("cd", help="create info", description= "BE AWESOME")
    # init_subparser.add_parser("config", help="create info", description= "BE AWESOME")
    # init_subparser.add_parser("config", help="create info", description= "BE AWESOME")


    # Create env ---------------
    env_sp = env.add_subparsers(title="subcommands",
                                description="valid tools for env",
                                # parser_class=argparse.ArgumentParser,
                                # action='help',
                                )

    env_create = env_sp.add_parser("create", help= "create new environment")
    env_list = env_sp.add_parser("list", help= "list all the available environments")
    env_info = env_sp.add_parser("info", help= "show information for selected env")
    env_delete = env_sp.add_parser("delete", help= "delete selected environment")

    # Parameters 
    env_create.add_argument("env:create:environment_name", metavar="env_name", help="environment name to create (no spaces)")
    env_info.add_argument("env:info:environment_name", metavar="env_name", help="show info for environment")
    env_delete.add_argument("env:delete:environment_name", metavar="env_name", help="delete selected environment")


    # Create env ---------------
    # create_env.add_argument("env-name", help="environment name to create")

    args = parser.parse_args()
    args_dict = args.__dict__
    
    # env_keys = env_create.parse_args()
    if "env:info:environment_name" in list(args_dict):
        print("available environments")

    if "env:create:environment_name" in list(args_dict):
        print("creating environment:")
        n = int(input("- Number of agents for the environment: "))
        print("")
        for agent in range(n): 
            print(f">Agent-{agent + 1}")
            agent_name = input(" -Agent name: ")
            obs_order = input(" -Obs order: ")
            can_see = input(" -Can see: ")

        print("create environment with name: %s" % (args_dict["env:create:environment_name"]))
        # print("env-summary: ") 
   
if __name__ == "__main__":
    cli()