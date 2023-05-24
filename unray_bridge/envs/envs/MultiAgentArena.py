from unray_bridge.envs.spaces import BridgeSpaces
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from ray.rllib.env import ExternalEnv
from unray_bridge.multiagents_config import MultiEnvCreator


env_config  = {
        "agent-1":{
            "observation": BridgeSpaces.MultiDiscrete([64, 64]),
            "action": BridgeSpaces.Discrete(4),
            "can_show": 1, # Amount of observations int obs stack
            "can_see": 2, # Amount of observations required in training 
            "obs_order": {   
                "agent-1": [0], 
                "agent-2": [0]
            }
        }, 
        "agent-2":{
            "observation": BridgeSpaces.MultiDiscrete([64, 64]),
            "action": BridgeSpaces.Discrete(4),
            "can_show": 1, # Amount of observations int obs stack
            "can_see": 2,
            "obs_order": {
                "agent-2": [0], 
                "agent-1": [0]
            }
        }
    }

def get_config():
    return env_config

def get_env(_ip = 'localhost', _port=10011, instance = False, amount_of_envs = 1):
    if amount_of_envs > 1:
        MCE = MultiEnvCreator(get_config(), amount_of_envs= amount_of_envs )
        env_config = MCE.get_multienv_config_dict()
    else:
        env_config = get_config()

    if instance:
        return MultiAgentBridgeEnv(
        name = "MultiAgentEnv", 
        ip = _ip,
        port = _port,
        config = env_config,
        first_connection = False
    )

    return lambda config: MultiAgentBridgeEnv(
        name = "MultiAgentEnv", 
        ip = _ip,
        port = _port,
        config = env_config,
        first_connection = False
    )
