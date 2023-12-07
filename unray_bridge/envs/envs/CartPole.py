
from unray_bridge.envs.bridge_env import BridgeEnv
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.envs.spaces import BridgeSpaces

import numpy as np 

def get_env(_ip = 'localhost', _port=9443, instance = False, amount_of_envs = 1, ID = 0): 

    high = np.array(
                [
                    1000,
                    np.finfo(np.float32).max,
                    140,
                    np.finfo(np.float32).max,
                ],
                dtype=np.float32,
            )

    ## Configurations Dictionaries
    # Define all the observation/actions spaces to be used in the Custom environment 
    # BridgeSpaces area based from gym.spaces. Check the docs for more information 
    # on how to use then. 

    # for this example we are using a a BoxSpace for our observations and a 
    # Discrete space for our action space.


    obs_config = {
            "space": BridgeSpaces.Box(-high, high), 
            "description": "General coordinates of the cartpole"
        }

    act_config = {
            "space": BridgeSpaces.Discrete(2), 
            "description": "General coordinates of the cartpole"
    }
    config_cartpole = {
        
        "observation": BridgeSpaces.Box(-high, high),
        "action": BridgeSpaces.Discrete(2),
        
    }

    # Create an instanec of the bridgeEnv defining parameters.

    return lambda config: BridgeEnv(
        name = "CartpoleEnv", 
        ip = _ip,
        port = _port,
        config = {
            "observation": obs_config, 
            "action": act_config
        },
        first_connection = False,
    )
