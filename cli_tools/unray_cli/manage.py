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
import argparse, os
from os import environ

import sys
import time
import threading
import webbrowser, http
from http.server import HTTPServer, SimpleHTTPRequestHandler
from flask_cors import CORS, cross_origin

from flask import Flask, render_template, send_from_directory,jsonify
import json
ip = "127.0.0.1"
port = 5000
url = f"http://{ip}:{port}"

app = Flask(__name__, static_folder='/Users/amoralesma/Documents/Nullspace/unray-bridge/unray-dashboard/build/static', template_folder="/Users/amoralesma/Documents/Nullspace/unray-bridge/unray-dashboard/build")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    root_dir = app.root_path
    return send_from_directory(root_dir + '/build', filename)

@app.route('/api/envs', methods=['GET'])
@cross_origin()
def get_users():
    with open('/Users/amoralesma/Documents/unray/envs/database.json', 'r') as f:
        data = json.load(f)
    return jsonify(data['envs'])

def start_server():
    # server_address = (ip, port)
    # httpd = HTTPServer(server_address, Handler)
    # Get info 

    app.run()
    # httpd.serve_forever()


def cli():
    DIR_PATH = "/Users/{}/Documents/unray".format(os.environ["USER"])

    # Check if config is set 
    if not environ.get('UNRAY_CONFIG_DIR') and not os.path.exists(DIR_PATH):
        print("")
        print("Well...There is not config detected for unray. If this is your first time using the tool, you have to setup the main config dir first.")
        response = input("Want to setup unray? (Y/N) ")
        if response.capitalize() == 'Y':
            print("---")
            dir = input("* \033[1m main unray-folder? (~/Documents/unray) \033[0m")
            
            
            if not os.path.exists(DIR_PATH):
                os.makedirs(DIR_PATH)
                os.makedirs(DIR_PATH + "/envs")
                os.makedirs(DIR_PATH + "/config")

                print("---")
                print(f"* [1/3] Main directory created at [{DIR_PATH}]")
                print(f"* [2/3] environments directory created")
                print(f"* [3/3] config directory created")
                print(f"---")

                os.environ["UNRAY_CONFIG_DIR"] = DIR_PATH # set the environment variable
                print("environment variable set!")
            else:
                print("directory already created!")
            
                
        return

    parser = argparse.ArgumentParser(
                        prog='unray',
                        description='Helps with general tasks for the tool',
                        epilog='Made <3 by Nullspace')
    
    subparser = parser.add_subparsers()
    
    init = subparser.add_parser("init", help="init new environment for unray_bridge")
    dashboard = subparser.add_parser("dashboard", help="crate a dashboard server")
    dashboard.set_defaults(dashboard=True)
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
    print(args_dict)
    if "dashboard" in list(args_dict):
        print("Starting server at port 9000")
        CURRENT_PATH = os.getcwd()
        DASHBOARD_PATH = os.path.join(CURRENT_PATH, "test")

        threading.Thread(target=start_server).start()
        webbrowser.open_new(url)

    

    if "env:info:environment_name" in list(args_dict):
        print("available environments")

    if "env:create:environment_name" in list(args_dict):
        print("Unray Environment Creator")
        print("---")
        print("[INTERACTIVE] You will be able to create your own unray_bridge environment definition. For more information on the parameters of the environment, visit https://github.com/Nullspace-Colombia/unray-bridge\n\n")
        
        n = int(input("- Number of agents for the environment: "))
        print("")
        for agent in range(n): 
            print(f"> Agent-{agent + 1}")
            agent_name = input("  - Agent name: ")
            obs_order = input("  - Obs order: ")
            can_see = input("  - Can see: ")

        print("create environment with name: %s" % (args_dict["env:create:environment_name"]))
        # print("env-summary: ") 
   
if __name__ == "__main__":
    cli()