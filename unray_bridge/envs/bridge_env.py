""" 
    BridgeEnv

    Definition of Main Bridge Envs that allow to communicate 
    with socket to send actions and receive observations from 
    UnrealEngine5 (UE5)

    There are two (2) main BridgeEnvironments. The SingleAgent 
    and the MultiAgent Environment 
    
    -   BridgeEnv 
    -   MultiAgentBridgeEnv

    In order to create a custom env, you have to inherit this 
    environments and createa (MultiAgent)BridgeEnv instance 
    with a initial configuration. 

    You ahve to define a observation_space and actions_space from 
    BridgeSpaces (@see unray_bridge.envs.spaces).

    @author Valentina Hernandez
    @author Andrés Morales 

    @version: 0.1V
    
    @file bridge_env.py 

"""
from .bridge.TCP_IP_Connector import ClientHandler
from unray_bridge.envs.spaces import BridgeSpaces
from unray_bridge import gui 
from gymnasium import Env as gymEnv
from ray.rllib.env.multi_agent_env import MultiAgentEnv

import gymnasium.spaces as spaces
import numpy as np

class BridgeEnv(gymEnv): 
    """
        Base class for custom UE5 Conenction. 
    """
    # 1. Custom gymenv metadata for viz. 
    metadata = {
        "rendermodes": [""], 
        "render_fps": ""
    }

    def __init__(self, 
                 name, 
                 ip, 
                 port, 
                 config, 
                 first_connection = False, 
                 validation = False, 
                 multiagent = False):
                 
        self.ip = ip # IP Address for IP Connection 
        self.port = port 
        
        if not name:
            print("error")
            raise ValueError("no environment name defined. Please define a name for tour environment on the BridgeEnv constructor.")
        self.name = name # environment name for later id 


        self.observation_config = config["observation"]
        self.action_config = config["action"]

        self.has_handler = False # ClientHandler to begin with connection
        self.has_connection = False

        self.validation = validation
        self.multiagent = multiagent 

        self.obs = [0]
        try: 
            self.observation_space = self.observation_config["space"] # Get imported space 
            self.action_space = self.action_config["space"]
        except: 
            raise ValueError("No correct space selected")

        # if first_connection:
        #     self.handler = ClientHandler(self.ip, self.port)

        self.create_handler()

    
    def step(self, action): 

        if not self.has_connection:
            self.connect()

        action=np.array(action,dtype=np.single)

        if isinstance(action, list): 
            action = np.array(action)
        elif isinstance(action, np.ndarray):
            pass
        else:
            assert "No valid action type. Only supports <list> or <numpy.ndarray> given %s" % (type(action))
        
        obs = self.obs 

        #terminated = self.check_termination(obs) # Check for validation to continue 
        #action = np.insert(action, 0, np.single(terminated))
        
        print('[ACTION]', end=" ")
        print(action)

        # 2. Cast the action vector to a byte buffer for send.
        action_buff = action.tobytes()
        n = self.get_amount_obs()
        # 3. Send the action vector to the environment. 
        self.handler.send(action_buff) # Send action an wait response 
        data_size = 8*(n+2)

        state = self.handler.recv(data_size) # Get state vetor 
        obs = state[0:n]
        self.obs = obs 
       
        # 4. Rewards System
        # For each frame within the termination limits, 
        ##reward = self.counter
        
        reward = state[n]
        terminated = bool(state[n+1])

        

        # 4. Rewards System
        # For each frame within the termination limits, 
        # self.counter += 1
        # reward = self.counter
        #reward = 0

        # Additional metadata [ignore ]
        truncated = False
        info = {}

        return obs, reward, terminated, truncated, info

    
    def reset(self, *, seed=None, options=None):
        print('[OBS]:', self.get_amount_obs())
        return np.zeros((self.get_amount_obs(),), dtype = np.double), {}

    def get_multiagent_state_dict(received_vector: np.array): 
        state = {}

        return 
    def check_termination(self, obs):
        """
            Check Termination 
            ---
            Verify if the episode must continue under a set of conditions 

        """
        terminated = False

        return terminated

    def get_amount_obs(self):
        return self.observation_space.shape[0]
    
    def which_observation(self): 
        """
            Which Obs
            ---
            Print description of the observation space in the environment. 
            Amount of elements per observation and fundamental structure. 
        """
        print(f"action dim: {self.observation_space}")

    def which_action(self): 
        """
            Which Obs
            ---
            Print description of the observation space in the environment. 
            Amount of elements per observation and fundamental structure. 
        """
        print(f"action dim: {self.action_space_dim}")

    def summary(self) -> None: 
        """
            Summary
            ---
            Prints the basic structure of the given space. Observation and 
            Actions structures, environment nameid and metadata 
        """
        TEXT_OFFSET = 80
        
        print("")
        print("THIS IS A AUTOGENERATED SUMMARY FOR THE CUSTOM BRIDGE ENV")
        print("--- ")

        print("\nEnvironment: \"{}\"".format(self.name))
        print("This is a gymnasium environment that connects to UE5 via TCP/IP")
        print(f"ip address: {self.ip}\t\t port: {self.port}")
        print("_" * TEXT_OFFSET)
        print("Feature\t\t\t\tType\t\t\t\tShape")
        print("=" * TEXT_OFFSET)

        print("Observation\t\t\t{}\t\t\t\t{}".format(
            self.get_space_type_instance(self.observation_space), # self.get_space_type_id(self.observation_config["type"]),
            self.observation_space.shape)
            )
        
        print("Action\t\t\t\t{}\t\t\t\t{}".format(
              self.get_space_type_instance(self.action_space), # self.get_space_type_id(self.observation_config["type"]),
             self.action_space.shape)
            )
        print("_"* TEXT_OFFSET)        
        print("")

    
    def get_space_type_instance(self, is_instance_object):
        """
            Get space type from instance. 

            Take the space instance. Depending on its class, returns a string 
            identificator the representes the given space. 

            Arguments 
            ---
            - is_instance_object: instance of the space class to compare 

            Returns
            ---
            - String identificator of the space to convert. 

        """
        if isinstance(is_instance_object, BridgeSpaces.Box):
            return "Box Space"
        elif isinstance(is_instance_object, BridgeSpaces.Discrete):
            return "Discrete Space"
    
        return "N/A"

    def create_handler(self): 
        self.handler = ClientHandler(self.ip, self.port) # Create a Handler 
        self.has_handler = True 

    def validate_handler(self): 
        return self.has_handler

        
    def connect(self):
        if self.has_handler:
            self.has_connection = self.handler.connect()
        
        
    def shutdown_server(self):
        """
            Shutdown Server 
            ---

        """
        self.handler.close()
    
class MultiAgentBridgeEnv(BridgeEnv, MultiAgentEnv):
    """
        MultiAgentBridgeEnv
    """
    def __init__(self, 
                 name: str, 
                 ip: str, 
                 port: int, 
                 config: dict, 
                 first_connection = False, 
                 validation = False, 
                 multiagent = False,
                 show_gui = True):
        
        # gui 
        if show_gui:
            gui.print_title()

        self.ip = ip # IP Address for IP Connection 
        self.port = port 
        
        if not name:
            print("error")
            raise ValueError("no environment name defined. Please define a name for tour environment on the BridgeEnv constructor.")
        self.name = name # environment name for later id 

        # get all agents names 
        self.agent_names = [] # get all agents names 
        self.observations = {}
        self.actions = {}

        for agent_name in config:
            self.agent_names.append(agent_name)
            self.observations[agent_name] = config[agent_name]["observation"]
            self.actions[agent_name] = config[agent_name]["action"]

        print("Multiagent params --")
        print(" - Agent names: {}".format(self.agent_names))
        print(" - Observations: {}".format(self.observations))
        print(" - Actions: {}".format(self.actions))
        print(" ")

        self.has_handler = False # ClientHandler to begin with connection
        self.has_connection = False

        self.validation = validation
        self.multiagent = multiagent 

        # Rllib metadata
        self.observation_space = self.observations['agent-1']
        self.action_space = self.actions['agent-1']


        self.obs = [0]

        self.create_handler()

    def get_amount_agents(self) -> int: 
        """
            Get Amount Agents
            ---
            Returns de amount of agents in the multiagent environment.

            @returns amount of agent names (int)
        """
        return len(self.agent_names)

    def validate_actions_dict(self, actions: dict) -> bool:
        """
        Validate Actions Dict
        ---
        Args:
            actions (dict): [description]

        Returns:
            bool: [description]
        """
        return len(actions) == self.get_amount_agents() 
    
    def to_byte(self, byte):
        """
            To byte
            ---
            Convert byte to bits for buffer sned 
        """
        return 8 * byte


    def get_dict_template(self):
        """
            get dict template 
            ---
            Get an agent-name dictionary for using as structure to 
            send to RLLib.
        """
        agent_dict_template = {}
        for agent in self.agent_names:
            agent_dict_template[agent] = ""

        return agent_dict_template
        
        
    def step(self, actions: dict) -> None:
        """
        Step 
        ---
        args:
            - action (dict): 
        
        """
        
        if not self.validate_actions_dict(actions):
            
            raise ValueError("Check the actions dict. Amount of agents do not match amount of actions send")

        if not self.has_connection:
            self.connect()

        print(actions)

        # create format 
        action2send = []
        for action in actions:
            action2send.append(actions[action])
            
        print(action2send) 

        action=np.array(action2send,dtype=np.single)

        if isinstance(action, list): 
            action = np.array(action)
        elif isinstance(action, np.ndarray):
            pass
        else:
            assert "No valid action type. Only supports <list> or <numpy.ndarray> given %s" % (type(action))
        
        obs = self.obs 

        #terminated = self.check_termination(obs) # Check for validation to continue 
        #action = np.insert(action, 0, np.single(terminated))
        
        print('[ACTION]', end=" ")
        print(action)
        

        total_obs_size = 0 # sizes 
        total_obs = []

        for idx, observation in enumerate(self.observations):
            observation_space = self.observations[observation] # discrete space 
            # print(f"Observation {idx}: {observation_space.shape[0]}" )
            # print(f"type: {type(observation_space)}")

            total_obs_size += observation_space.shape[0]
            total_obs.append(observation_space.shape[0])

        # print("observaciones totales: ", total_obs_size)
        # print("agentes: ", self.get_amount_agents())

        # print("dictionary: ")
        # print(self.get_dict_template())

        # 2. Cast the action vector to a byte buffer for send.
        action_buff = action.tobytes()
        # n = self.get_amount_obs()
        # 3. Send the action vector to the environment. 
        self.handler.send(action_buff) # Send action an wait response 
        

        # estructura:   (id + obs + reward + done) * agente 
        data_size = self.to_byte(total_obs_size + self.get_amount_agents() * 3) # bytes from read 
        
        # calculate the size get the type of size 
        
        state = self.handler.recv(data_size) # Get state vetor 
        # print(f"[STATE FROM UE] {state}")
                                
        obs_dict = self.get_dict_template() # from agents names 
        reward_dict = self.get_dict_template() # from agents names 
        done_dict = self.get_dict_template() # from agents names 
        truncated_dict = self.get_dict_template() # from agents names 

        
        acum = 0
        all_done = True

        for idx, n in enumerate(total_obs):
            # extract agent parameters for episode 
            obs = state[acum:acum + n]
            reward = state[-(self.get_amount_agents() - idx)]
            done = state[-(2 * self.get_amount_agents() - idx)]
            
            current_agent_name = self.agent_names[idx] # agent name from dicitonary 

            # update each dictionary from major data 
            obs_dict[current_agent_name] = obs
            reward_dict[current_agent_name] = reward
            done_dict[current_agent_name] = done 
            truncated_dict[current_agent_name] = False

            all_done = all_done and done 

            acum += n

        # New structure design
        # accum = 0
        # for idx, agent in enumerate(self.agent_names):
        #     id = state[idx]
        #     obs = state[:]
        #     reward[state[]]

        done_dict["__all__"] = all_done 

        # create dictionary 
        
        self.obs = obs_dict
        
    
        # 4. Rewards System
        # For each frame within the termination limits, 
        ##reward = self.counter
        
        # reward = state[n]
        # terminated = bool(state[n+1])

        

        # 4. Rewards System
        # For each frame within the termination limits, 
        # self.counter += 1
        # reward = self.counter
        #reward = 0

        # Additional metadata [ignore ]
        truncated = False
        info = {}

        return obs_dict, reward_dict, done_dict, truncated_dict, info
    

    def reset(self, *, seed=None, options=None):
        print('[OBS]:', self.obs)
        obs_dict = self.get_dict_template() # from agents names 
        for agent in obs_dict:
            obs_dict[agent] = np.array([0, 0])
        return obs_dict, {}



    




