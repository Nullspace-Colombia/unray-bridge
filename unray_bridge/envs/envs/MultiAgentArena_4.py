from unray_bridge.envs.spaces import BridgeSpaces
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from ray.rllib.env import ExternalEnv

def get_env(_ip = 'localhost', _port=10011, instance = False):
    env_config  = {
        "agent-1":{
            "observation": BridgeSpaces.MultiDiscrete([64, 64]),
            "action": BridgeSpaces.Discrete(4),
            "can_show": 1,
            "can_see": 2,                        
            "obs_order": {   
                "agent-1": [0], 
                "agent-2": [0]
            }
        }, 
        "agent-2":{
            "observation": BridgeSpaces.MultiDiscrete([64, 64]),
            "action": BridgeSpaces.Discrete(4),
            "can_show": 1,
            "can_see": 2,
            "obs_order": {
                "agent-2": [0], 
                "agent-1": [0]
            }
        },
        "agent-3":{
            "observation": BridgeSpaces.MultiDiscrete([64, 64]),
            "action": BridgeSpaces.Discrete(4),
            "can_show": 1,
            "can_see": 2,
            "obs_order": {
                "agent-3": [0], 
                "agent-4": [0]
            }
        },
        "agent-4":{
            "observation": BridgeSpaces.MultiDiscrete([64, 64]),
            "action": BridgeSpaces.Discrete(4),
            "can_show": 1,
            "can_see": 2,
            "obs_order": {
                "agent-4": [0], 
                "agent-3": [0]
            }
        }
    }

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