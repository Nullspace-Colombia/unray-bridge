from unray_bridge.envs.bridge.TCP_IP_Connector import ClientHandler
from unray_bridge.multiagents_config import MultiEnvCreator
# from data_handler import DataHandler
import numpy as np
from unray_bridge import gui
import threading
import queue
import ray


@ray.remote
class Bridge():
    def __init__(self, env_config, n_envs=1, ip='localhost', port=10010, show_gui=True):
        self.ip = ip
        self.port = port
        self.client_handler = ClientHandler(self.ip, self.port)
        self.is_connected = False
        self.consock = None
        self.n_envs = n_envs
        self.MCE = MultiEnvCreator(env_config, amount_of_envs=self.n_envs)
        self.n_obs = self.get_nobs()
        self.action_dict_2_send = {}
        self.consock = self.client_handler.set_socket()
        self.send_state = False
        self.data = []
        self.tick_count = 0
        self.TICK_INTERVAL = 0.01  #  segundos
        self.clock_tick()
        self.sent_ID = -1
        self.action_queue = queue.Queue()

        # if show_gui:
        # gui.print_title()
        print(f"---------[BRIDGE CREADO]---------------{id(self)}")
        # self.data_handler = DataHandler()

    def get_client_handler(self):
        return self.client_handler

    def clock_tick(self):
        if self.tick_count > 1:
            print("count: {}".format(self.tick_count))
            
            self.send_queue_action()
        self.tick_count = self.tick_count + 1
        threading.Timer(self.TICK_INTERVAL, self.clock_tick).start()
        return

    def get_data_handler(self):
        return self.data_handler



    def set_queue_action(self, current_env_obs): 
        """
        
        """
        self.action_queue.put(current_env_obs)
        print("[ACTION QUEUE ] added new act vect, current size {}".format(self.action_queue.qsize()))

    def get_queue_action_size(self):
        return self.action_queue.qsize()


    def send_queue_action(self):
        """
            Send action_stack from queue
            ---
            Get the action_stack for a given environment 
            to be send to the UE scene. This will send the 
            environment id with the required actions. 

            [OLNY FOR ONE ENVIRONMENT]
        """
        if self.action_queue.qsize() <= 0:
            return False #TODO: Raise exception 
        
        action_stack_to_send = self.action_queue.get()  #  action to send to UE5
        env_id = action_stack_to_send[0]
        
        print("[ACTION STACK ID] {}".format(env_id)) # env 

        try:
            
            self.data = self.send_data(action_stack_to_send)
            self.sent_ID = action_stack_to_send[0]
            print(f"SENDING DATA: {action_stack_to_send}")
        except:
            print("DID NOT SEND DATA")
            return False
        
        return True

    def start(self):

        print(f"SOCKET ID IN START {id(self.consock)}")
        print("[CONNECTING CLIENT]")
        try:
            self.client_handler.connect(self.consock)
            print("[CLIENT CONNECTED]")
        except:
            print("FAILED TO CONNECT CLIENT :(")
        self.is_connected = True
        # self.consock = conn_sock

    def set_actions(self, action, env_ID):
        """
            Set actions 
            ---
            Llamado desde cada entorno para apilar el vector de 
            acciones antes del envio (Paralelizacion)
        """

        print(f"[SETTING ACTIONS]: ENV {env_ID}")
        self.action_dict_2_send[str(env_ID)] = action
        print(self.action_dict_2_send)
        print(f"[# ACTIONS]: {len(self.action_dict_2_send.keys())}")

        print(f"[SENDING ACTIONS]")
        self.send_actions()

        #  self.send_actions()

    def get_send_state(self):
        return self.send_state

    def get_sent_id(self):
        return self.sent_ID


    def send_actions(self):
        """
            Buffer de Envio 
        """
        #  Conversion de diccionario a buffer
        buffer2send = []
        for key_id in range(self.n_envs):
            buffer2send.extend(self.action_dict_2_send[str(key_id + 1)])

        #  action_buff = self.actions.tobytes()
        action_buff = np.asarray(buffer2send, dtype=np.single).tobytes()
        print(f"SOCKET ID IN SEND {id(self.consock)}")
        self.client_handler.send(action_buff, self.consock)
        print("RECEIVING DATA")
        self.recv_data()
        print("DATA RECEIVED")

    def get_state(self, env_id):
        #print(f"[GETTING STATE]: {self.data}")
        num_obs = self.to_byte(self.get_nobs()+self.get_amount_agents() * 3)
        n_obs = 8  #  check :v
        print(
            f"-------------------------------SLICE DESDE:{(env_id - 1)* n_obs} hasta {env_id * n_obs} para entorno {env_id}-------------")
        #  Porcion de observacion por entorno
        env_data = self.data[(env_id - 1) * n_obs: env_id * n_obs]

        print(f"[ENV DATA]: {env_data}")
        return env_data

    def get_state_stack(self):
        print(f"[GETTING STATE]: {self.data}")
        return self.data
    
    def set_socket(self):
        print("SETTING SOCKET")
        try:
            self.consock = self.client_handler.set_socket()
            print(f"..............SOCKET FROM HANDLER----------{self.consock}")
            print(f"SOCKET ID IN SETSOCKET {id(self.consock)}")
            return self.consock

        except:
            print("COULDNT SET SOCKET :(")

    def get_socket(self):
        return self.consock

    def recv_data(self, given_socket = False):
        """
            Recive observaciones. TODO: Change name to recv_obs
        """

        data_size = self.to_byte(
            self.n_obs+self.get_amount_agents() * 3)  # bytes from read
        self.data = self.client_handler.recv(data_size, self.consock)
        print(f"[DATA]: {self.data}")
        return self.data

    def select_obs_per_env(self, env_id):
        print(f"[GETTING STATE]: {self.data}")
        num_obs = self.to_byte(self.get_nobs()+self.get_amount_agents() * 3)
        n_obs = num_obs // self.n_envs  #  check :v
        #  Porcion de observacion por entorno
        env_data = self.data[env_id * (n_obs - 1): env_id * n_obs - 1]

        return env_data

    def get_amount_workers_active(self):
        return 3

    def get_nactions(self):
        self.multienv_config = self.MCE.get_multienv_config_dict()
        self.agents_names = list(self.multienv_config.keys())
        n_actions = sum([self.multienv_config[agent]['action'].shape[0]
                        for agent in self.multienv_config])
        # estructura:   (id + obs + reward + done) * agente
        return n_actions

    def get_nobs(self):
        self.multienv_config = self.MCE.get_multienv_config_dict()
        self.agents_names = list(self.multienv_config.keys())
        n_obs = sum([self.multienv_config[agent]['can_show']
                    for agent in self.multienv_config])

        # estructura:   (id + obs + reward + done) * agente
        return n_obs

    def to_byte(self, byte):
        """
            To byte
            ---
            Convert byte to bits for buffer sned 
        """
        return 8 * byte

    def get_amount_agents(self) -> int:
        """
            Get Amount Agents
            ---
            Returns de amount of agents in the multiagent environment.

            @returns amount of agent names (int)
        """
        return len(self.agents_names)

    def send_data(self, buffer2send, verbose=False):
        """
            send data through socket
            ---
            @args buffer2send {np.array} - array to be converted and send to UE5 
            @returns recv_data {np.array} - data send as response from socket 
        """
        try:
            action_buff = np.asarray(buffer2send, dtype=np.single).tobytes()
            self.client_handler.send(action_buff, self.consock)
            self.data = self.recv_data()
        except:
            return []

        return self.data
    """
    def has_socket(self):
        if self.client_handler.sock is None:
            return False
        else:
            return True
    """
