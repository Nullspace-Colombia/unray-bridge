from unray_bridge.envs.bridge.TCP_IP_Connector import ClientHandler
from unray_bridge.multiagents_config import MultiEnvCreator
#from data_handler import DataHandler


class Bridge():
    def __init__(self, env_config, n_envs = 1, ip = 'localhost', port = 10010):
        self.ip = ip
        self.port = port
        self.client_handler = ClientHandler(self.ip, self.port)
        self.is_connected = False
        self.sock = None
        self.MCE = MultiEnvCreator(env_config, amount_of_envs= n_envs)
        self.n_obs = self.get_nobs()
        self.n_evs = n_envs

        self.action_dict_2_send = {}

        #self.data_handler = DataHandler()

    def get_client_handler(self):
        return self.client_handler
    
    def get_data_handler(self):
        return self.data_handler
    
    def start(self, sock):
        self.sock = sock
        self.client_handler.connect(sock)
        self.is_connected = True

    def set_actions(self, action, env_ID):
        """
            Set actions 
            ---
            Llamado desde cada entorno para apilar el vector de 
            acciones antes del envio (Paralelizacion)
        """

        if len(self.action_dict_2_send.keys()) >= self.n_evs:
            self.send_actions() 
        else: 
            self.action_dict_2_send[str(env_ID)] = action
        # self.send_actions()

    def send_actions(self):
        """
            Buffer de Envio 
        """
        # Conversion de diccionario a buffer 
        buffer2send = []
        for key_id in range(self.n_evs):
            buffer2send.extend(self.action_dict_2_send[str(key_id + 1)])
            
        # action_buff = self.actions.tobytes()
        action_buff = buffer2send.tobytes()
        self.client_handler.send(action_buff, self.sock)
    
    def get_state(self, ID):        
        return self.select_obs_per_env(ID)
    
    def set_socket(self):
        sock = self.client_handler.set_socket()
        return sock
        
    def get_socket(self):
        return self.sock

    def recv_data(self):
        """
            Recive observaciones. TODO: Change name to recv_obs
        """
        data_size = self.to_byte(self.n_obs+self.get_amount_agents() * 3) # bytes from read 
        self.data = self.client_handler.recv(data_size, self.sock)
        
    def select_obs_per_env(self, env_id):
        n_obs = self.get_nobs() / self.n_evs # check :v 
        env_data = self.data[env_id * (n_obs - 1): env_id * n_obs - 1] # Porcion de observacion por entorno 
        return env_data 

    def get_amount_workers_active(self): 
        return 3
    
 
    def get_nactions(self):
        self.multienv_config = self.MCE.get_multienv_config_dict()
        self.agents_names = list(self.multienv_config.keys())
        n_actions = sum([self.multienv_config[agent]['action'].shape[0] for agent in self.multienv_config])
        # estructura:   (id + obs + reward + done) * agente 
        return n_actions
    
    def get_nobs(self):
        self.multienv_config = self.MCE.get_multienv_config_dict()
        self.agents_names = list(self.multienv_config.keys())
        n_obs = sum([self.multienv_config[agent]['can_show'] for agent in self.multienv_config])
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
    
    def send_data(self):
        pass
    """
    def has_socket(self):
        if self.client_handler.sock is None:
            return False
        else:
            return True
    """ 

    
    
    

    