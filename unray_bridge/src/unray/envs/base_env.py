from unray.envs.bridge_env import BridgeEnv
from unray.envs.bridge_env import MultiAgentBridgeEnv

class SingleAgentEnv():
    def __init__(self, config, env_name, ip = 'localhost' , port = 9443):
        self.env_ip = ip
        self.env_port = port
        self.env_config = config
        self.name = env_name

    def get_env(self):
        return lambda config: BridgeEnv(
            name = self.name, 
            ip = self.env_ip,
            port = self.env_port,
            config = self.env_config,
            first_connection = False,
        )
    
    def get_name(self):
        return self.name

class MultiAgentEnv(SingleAgentEnv):
    def __init__(self, config, env_name, ip='localhost', port=9443, ID = 1):
        super().__init__(config, env_name, ip, port)
        self.ID = ID

    def get_env(self):
        return lambda config: MultiAgentBridgeEnv(
            name = self.name, 
            ip = self.env_ip,
            port = self.env_port,
            config = self.env_config,
            first_connection = False,
            ID = self.ID,
        )
    
    def get_name(self):
        return self.name


