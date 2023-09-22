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

    You have to define a observation_space and actions_space from 
    BridgeSpaces (@see unray_bridge.envs.spaces).

    @author Valentina Hernandez
    @author Andrés Morales 

    @version: 0.1V
    
    @file bridge_env.py 

"""
from .bridge.TCP_IP_Connector import ClientHandler
from unray_bridge.envs.spaces import BridgeSpaces
from gymnasium import Env as gymEnv
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from unray_bridge.bridge import Bridge
import ray
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

        
        try: 
            self.observation_space = self.observation_config["space"] # Get imported space 
            self.action_space = self.action_config["space"]
        except: 
            raise ValueError("No correct space selected")

        self.obs = self.observation_space.sample()
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
        return np.asarray(self.obs, dtype=self.observation_space.dtype), {}

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
                 #Paralell
                 ID = int,
                 bridge= None):
        
        # gui 
        

        self.ip = ip # IP Address for IP Connection 
        self.port = port 
        #self.bridge = env_bridge
        if bridge is not None:
            self.bridge = bridge
            print(f"---------- BRIDGE: {id(self.bridge)}------------")

        if not name:
            print("error")
            raise ValueError("no environment name defined. Please define a name for tour environment on the BridgeEnv constructor.")
        self.name = name # environment name for later id 

        # get all agents names 
        self.agent_names = [] # get all agents names 
        self.observations = {}
        self.actions = {}
        self.can_sees = {}
        self.obs_order = {}
        self.reset_count = 0

        # for agent_name in config:
        #     self.agent_names.append(agent_name)
        #     self.observations[agent_name] = config[agent_name]["observation"]
        #     self.actions[agent_name] = config[agent_name]["action"]
        #     self.can_sees[agent_name] = config[agent_name]["can_see"]
        #     self.obs_order[agent_name] = config[agent_name]["obs_order"]

        
        self.agents_names = list(config.keys())
        print(f"Agents: {self.agents_names}")
        #print(f"ID: {self.ID}")

        # print("Multiagent params --")
        # print(" - Agent names: {}".format(self.agent_names))
        # print(" - Observations: {}".format(self.observations))
        # print(" - Actions: {}".format(self.actions))
        # print(" - Can see: {}".format(self.can_sees))
        # print(" - Observation order: {}".format(self.obs_order))

        print(" ")

        self.has_handler = False # ClientHandler to begin with connection
        self.has_connection = False

        self.validation = validation
        self.multiagent = multiagent 

        # Rllib metadata
        self.obs_space_dict = self.get_dict_template()
        self.act_space_dict = self.get_dict_template()
        
        for idx, agent in enumerate(self.agents_names):
            self.obs_space_dict[agent] = config[self.agents_names[idx]]['observation']
            self.act_space_dict[agent] = config[self.agents_names[idx]]['action']  

        #print("-------------")  
        #print(self.act_space_dict)
        #print("-------")
        self.observation_space = config[self.agents_names[0]]['observation']
        self.action_space = config[self.agents_names[0]]['action']

        self.config = config # configuracion de entorno
        self.heads_reference = self.get_dict_template() # where the state vector begins 

        for idx, agent in enumerate(self.agents_names):
            print(self.config[agent])
            self.heads_reference[agent] = 1 if idx == 0 else self.heads_reference[prev_agent] + 3 + self.config[agent]['can_show']
            prev_agent = agent

        #print("Heads reference: ", end = "") 
        #print(self.heads_reference)
        
        ## Paralell
        #self.create_handler()
        ## paralell
        self.ID = ID

        self.has_connection = True
        self.has_handler = True
        #self.data_handler = self.bridge.get_data_handler()

        self.obs_dict = self.get_dict_template()
        self.dummy_action = self.get_dict_template()
        #if not self.bridge.has_socket():
        #    self.bridge.set_socket()
        
        

        

    def get_amount_agents(self) -> int: 
        """
            Get Amount Agents
            ---
            Returns de amount of agents in the multiagent environment.

            @returns amount of agent names (int)
        """
        return len(self.agents_names)

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
        for agent in self.agents_names:
            agent_dict_template[agent] = ""

        return agent_dict_template
        
        
    def step(self, actions: dict) -> None:
        """
        Step 
        ---
        args:
            - action (dict): 
        
        """
        print(f"[ACTIONS]:{actions}")
        print(f"[AGENTS]:{self.agents_names}")
        """
        if not self.validate_actions_dict(actions):
            
            raise ValueError("Check the actions dict. Amount of agents do not match amount of actions send")
        """
        # Paralell
        

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
        
        obs = self.obs_dict 


        #terminated = self.check_termination(obs) # Check for validation to continue 
        #action = np.insert(action, 0, np.single(terminated))
        
        print('[ACTION]', end=" ")
        print(action)
        

        total_obs_size = 0 # sizes 
        total_obs = []
        agents = self.observations.keys() # agents names
        print("agents:", end = " ") 
        print(agents) 

        can_sees_total = []
        order_observations = []

        # for idx, observation in enumerate(self.observations): 
        #     observation_space = self.observations[observation] # discrete space  for each agent 
        #     # print(f"Observation {idx}: {observation_space.shape[0]}" )
        #     # print(f"type: {type(observation_space)}")

        #     total_obs_size += observation_space.shape[0]
        #     total_obs.append(observation_space.shape[0]) # total space for observations 
        #     can_sees_total.append(self.can_sees[observation]) # arreglo de cansees 
        #     order_observations.append([e for e in self.obs_order[observation]])

        # print(can_sees_total)
        # print(order_observations)

             
        # for idx, agent_name in self.observations.keys(): 
        #     order_observations = self.observations[agent_name]
        #     amount_of_observations = self.can_sees[agent_name]
            

        # print("observaciones totales: ", total_obs_size)
        # print("agentes: ", self.get_amount_agents())

        # print("dictionary: ")
        # print(self.get_dict_template())

        # 2. Cast the action vector to a byte buffer for send.
        #action_buff = action.tobytes()
        # n = self.get_amount_obs()
        # 3. Send the action vector to the environment. 
        self.dummy_obs = self.get_dict_template()
        self.dummy_dones = self.get_dict_template()
        self.dummy_reward = self.get_dict_template()
        self.dummy_truncated = self.get_dict_template()
        ##Paralell
        #self.handler.send(action_buff) # Send action an wait response 
        #print(f"RESET COUNT: {self.reset_count}")
        if self.reset_count > 0:
            self.bridge.set_actions.remote(action, self.ID)
            self.bridge.set_queue_action.remote([self.ID, action])
            state_ray = self.bridge.get_state.remote(self.ID)
            state = ray.get(state_ray)
            print(f"[STATE]:{state}")
        else:
            for agent in self.agents_names:
            #print(f"{agent} ==== {self.act_space_dict[agent]}")
            #obs_dict[agent] = np.asarray(self.observation_space.sample(), dtype=self.observation_space.dtype)
                self.dummy_obs[agent] = self.obs_space_dict[agent].sample()
                self.dummy_dones[agent] = False
                self.dummy_reward[agent] = 0
                self.dummy_truncated[agent] = False 
            
        #n_obs = sum([self.config[agent]['can_show'] for agent in self.config])
        # estructura:   (id + obs + reward + done) * agente 
        #data_size = self.to_byte(n_obs + self.get_amount_agents() * 3) # bytes from read 
        
        # calculate the size get the type of size 
        """ 
        while True:
            if self.bridge.get_send_state.remote()== True:
                print("SENDINGGGGGGGGGGGGGGGGGG")
                break
        """       
        ##Paralell
        #state = self.handler.recv(data_size) # Get state vetor 
        
        # print(f"[STATE FROM UE] {state}")
                                
        obs_dict = self.get_dict_template() # from agents names 
        reward_dict = self.get_dict_template() # from agents names 
        done_dict = self.get_dict_template() # from agents names 
        truncated_dict = self.get_dict_template() # from agents names 

        
        acum = 0
        all_done = True


        # Read the specific observations vector 
        # 
        #  id = 1 
        #  obs = total_obs[idx]

        head = 0
        heads = []
        #print(f"RESET COUNT: {self.reset_count}")
        if self.reset_count > 0:
            for agent in self.agents_names:
                # amount of observations in the agent 
                obs_dict_arr = []
                for observation_check_agent in list(self.config[agent]['obs_order']):
                    for idx_observation_check_agent in self.config[agent]['obs_order'][observation_check_agent]:
                        print(f"Checking in {agent} state with {observation_check_agent} at position {idx_observation_check_agent}")            
                        obs_dict_arr.append(state[self.heads_reference[observation_check_agent]] + idx_observation_check_agent)
                
                reward_dict[agent] = state[self.heads_reference[agent] + self.config[agent]['can_show'] ] 
                done_dict[agent] =  bool(state[self.heads_reference[agent] + self.config[agent]['can_show'] + 1])
                #if done_dict[agent] == False:
                #obs_dict[agent] = np.asarray(obs_dict_arr, dtype=self.observation_space.dtype) # Add all states needed for agent 
                obs_dict[agent] = np.asarray(obs_dict_arr, dtype=self.obs_space_dict[agent].dtype) # Add all states needed for agent 
                #else:
                #    del obs_dict[agent]
                #    del done_dict[agent]
                truncated_dict[agent] = False
                if agent in done_dict:
                    all_done = all_done and done_dict[agent]
        else:
            obs_dict = self.dummy_obs
            reward_dict = self.dummy_reward
            done_dict = self.dummy_dones
            truncated_dict = self.dummy_truncated
            
            

        # for idx, n in enumerate(total_obs):
        #     # extract agent parameters for episode 
        #     skip = 3 + sum(total_obs[:idx])
        #     id = state[idx * skip]
        #     # obs = [state[1 + idx * skip: 1 + idx * skip + 1 ], state[1 + (idx + 1) * skip: 1 + idx * skip + 1 ]]#total_obs[idx]] # aqui es donde no cuadra
        #     obs = [2, 6] 
        #     reward = state[1 + idx * skip + 1 ]# total_obs[idx]]
        #     done = state[2 + idx * skip + 1] #  total_obs[idx]]
            
        #     current_agent_name = self.agent_names[idx] # agent name from dicitonary 

        #     # update each dictionary from major data 
        #     obs_dict[current_agent_name] = np.array(obs, dtype= np.int16)
        #     reward_dict[current_agent_name] = reward
        #     done_dict[current_agent_name] = bool(done)
        #     truncated_dict[current_agent_name] = False

        #     all_done = all_done and done 

        #     acum += n

        done_dict["__all__"] = bool(all_done )
        truncated_dict["__all__"] = False 

        # create dictionary 
        self.obs_dict = obs_dict

        info = {}

        print(" Dicts ")
        print("-obs: ")
        print(obs_dict, end = "\n \n")
        print("-reward: ")
        print(reward_dict, end = "\n \n")
        print("-done: ")
        print(done_dict, end = "\n \n")
        print("-truncated: ")
        print(truncated_dict, end = "\n \n")
        return obs_dict, reward_dict, done_dict, truncated_dict, info
    

    def reset(self, *, seed=None, options=None):
        """
            Reset
            ---

        """
        if self.dummy_action[self.agents_names[0]] == '':
            for agent in self.agents_names:
            #print(f"{agent} ==== {self.act_space_dict[agent]}")
            #obs_dict[agent] = np.asarray(self.observation_space.sample(), dtype=self.observation_space.dtype)
                self.dummy_action[agent] = self.act_space_dict[agent].sample()
            print(f"[DUMMY ACTION]: {self.dummy_action}")
            obs_dict, self.reward_dict, self.done_dict, self.truncated_dict, self.info = self.step(self.dummy_action)
        else:
            print('[RESETTING]')
            print('[OBS]:', self.obs_dict)
            obs_dict = self.get_dict_template() # from agents names 
            for agent in obs_dict:
                #obs_dict[agent] = np.asarray(self.observation_space.sample(), dtype=self.observation_space.dtype)
                obs_dict[agent] = np.asarray(self.obs_dict[agent], dtype=self.obs_space_dict[agent].dtype)
            print("- Obs_dict: ")
            print(obs_dict)
        self.reset_count = self.reset_count+1
        return obs_dict, {}
    
    def create_handler(self): 
        self.handler = ClientHandler(self.ip, self.port) # Create a Handler 
        self.has_handler = True 

    def set_bridge(self, conn_bridge):
        self.bridge = conn_bridge
        print(f"-------BRIDGE: {id(conn_bridge)}------------")
        return id(conn_bridge)

    def set_ID(self, ID):
        self.ID = ID
    
    def get_ID(self):
        return self.ID



