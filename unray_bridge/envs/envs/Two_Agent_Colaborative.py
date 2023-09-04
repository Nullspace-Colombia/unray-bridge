from gymnasium.spaces import Tuple
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from unray_bridge.multiagents_config import MultiEnvCreator
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv 
from unray_bridge.envs.spaces import BridgeSpaces
import numpy as np
class TwoAgentColaborative(MultiAgentEnv):
    def __init__(self,name,ip,port,env_config, first_connection):
        super().__init__()
        env = MultiAgentBridgeEnv(
        name = name, 
        ip = ip,
        port = port,
        config = env_config,
        first_connection = first_connection)

        no_agents = len(env_config.keys())
        tuple_obs_space = Tuple([env.observation_space]*no_agents)
        tuple_act_space = Tuple([env.action_space]*no_agents)

        self.env = env.with_agent_groups(
            groups={"agents1": list(env_config.keys())},
            obs_space=tuple_obs_space,
            act_space=tuple_act_space,
        )
        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space
        self._agent_ids = {"agents1"}
        self._skip_env_checking = True

    def reset(self, *, seed=None, options=None):
        return self.env.reset(seed=seed, options=options)

    def step(self, actions):
        
        return self.env.step(actions)


#observations are traces and the position of the agent
high = np.array(
            [3000]*19,
            dtype=np.float32,
        )
# actions are  : moving (X,Y, Rot Z, jump) and grab
env_config  = {
    "agent-1":{
        "observation": BridgeSpaces.Box(-high, high),
        "action": BridgeSpaces.Discrete(6),
        "can_show": 19, 
        "can_see": 19, 
        "obs_order": {   
            "agent-1": [i for i in range(19)], 
            "agent-2": []}
    }, 
    "agent-2":{
        "observation":BridgeSpaces.Box(-high, high),
        "action":BridgeSpaces.Discrete(6),
        "can_show": 19, # Amount of observations int obs stack
        "can_see": 19, # Amount of observations required in training 
        "obs_order": { 
            "agent-2": [i for i in range(19)],  
            "agent-1": []
            }
    }
}
def get_config():
    return env_config

def get_env(_ip = 'localhost', _port=10010, instance = False, amount_of_envs = 1):
    if amount_of_envs > 1:
        MCE = MultiEnvCreator(get_config(), amount_of_envs= amount_of_envs )
        env_config = MCE.get_multienv_config_dict()
    else:
        env_config = get_config()

    if instance:
        return TwoAgentColaborative(
        name = "TwoAgentColaborative", 
        ip = _ip,
        port = _port,
        env_config = env_config,
        first_connection = False
    )
    return lambda config: TwoAgentColaborative(
        name = "TwoAgentColaborative", 
        ip = _ip,
        port = _port,
        env_config = env_config,
        first_connection = False
    )