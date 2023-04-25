from unray_bridge.envs.spaces import BridgeSpaces
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv

def get_env(_ip = 'localhost', _port=10010):
    env_config  = {
        "agent-1":{
            "observation": BridgeSpaces.MultiDiscrete([64], [64]),
            "action": BridgeSpaces.Discrete(4),
        }, 
        "agent-2":{
            "observation": BridgeSpaces.MultiDiscrete([64], [64]),
            "action": BridgeSpaces.Discrete(4),
        }
    }

    return lambda config: MultiAgentBridgeEnv(
        name = "CartpoleEnv", 
        ip = _ip,
        port = _port
        config = env_config,
        first_connection = False
    )
