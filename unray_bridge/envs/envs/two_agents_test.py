from unray_bridge.envs.spaces import BridgeSpaces
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.multiagents_config import MultiEnvCreator
import numpy as np

high = np.array(
            [10000]*19,
            dtype=np.float32,
        )
env_config = {"agent-1": {
              "observation":BridgeSpaces.Box(-high, high),
              "action": BridgeSpaces.MultiDiscrete([2,2,3]),
              "can_show": 19, # Amount of observations int obs stack
              "can_see": 19, # Amount of observations required in training
              "obs_order": {'agent-1':[i for i in range(19)],'agent-2':[]}
              },
              "agent-2": {
              "observation":BridgeSpaces.Box(-high, high),
              "action": BridgeSpaces.MultiDiscrete([2,2,3]),
              "can_show": 19, # Amount of observations int obs stack
              "can_see": 19, # Amount of observations required in training
              "obs_order": {'agent-2':[i for i in range(19)]},'agent-1':[]}
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
        return MultiAgentBridgeEnv(
        name = "TwoAgentColab", 
        ip = _ip,
        port = _port,
        config = env_config,
        first_connection = False
    )
    return lambda config: MultiAgentBridgeEnv(
        name = "TwoAgentColab", 
        ip = _ip,
        port = _port,
        config = env_config,
        first_connection = False
    )



