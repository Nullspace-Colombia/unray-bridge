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

parser = argparse.ArgumentParser(
                    prog='Unray Manage Tools',
                    description='Helps with general tasks for the tool',
                    epilog='Made <3 by Nullspace')

parser.add_argument('create-env')
parser.add_argument('env-name')

args = parser.parse_args()
args_parsed = vars(args)
print(args_parsed)

will_create_env = args_parsed['create-env'] == 'create-env'
filename = args_parsed['env-name']

if will_create_env:
    src = "unray_bridge/envs/envs/template/CustomEnv.py" 
    dst = f"unray_bridge/envs/envs/{filename}.py" 
    shutil.copyfile(src, dst)
