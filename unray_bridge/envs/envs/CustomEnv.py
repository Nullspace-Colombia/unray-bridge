
from unray_bridge.envs.bridge_env import BridgeEnv
from unray_bridge.envs.spaces import BridgeSpaces

import numpy as np 
"""
def get_env(): 

    obs_config = {
            "space": # Space, 
            "description": #Description 
        }

    act_config = {
            "space": # Space, 
            "description": #Description 
    }

    # Create an instanec of the bridgeEnv defining parameters.

    return lambda config: BridgeEnv(
        name = "name", 
        ip = 'localhost',
        port = 0000,
        config = {
            "observation": obs_config, 
            "action": act_config
        },
    )
"""