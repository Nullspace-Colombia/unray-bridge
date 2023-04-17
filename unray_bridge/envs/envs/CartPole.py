
from unray_bridge.envs.bridge_env import BridgeEnv
from unray_bridge.envs.spaces import BridgeSpaces

import numpy as np 

# Limits for BoxSpace. 
# [Rx,Ry,Px,Py,Vax,Vay,Vx,Vy]

def get_env(): 

    high = np.array(
                [   140,
                    140,
                    1200,
                    1200,
                    np.finfo(np.float32).max,
                    np.finfo(np.float32).max,
                    np.finfo(np.float32).max,
                    np.finfo(np.float32).max
                ],
                dtype=np.float32,
            )
    high_act = np.array(
                [
                    1,
                    1
                ],
                dtype=np.float32,
            )

    obs_config = {
            "space": BridgeSpaces.Box(-high, high), 
            "description": "General coordinates of the cartpole"
        }

    act_config = {
            "space": BridgeSpaces.Box(-high_act, high_act), 
            "description": "General coordinates of the cartpole"
    }

    # Create an instanec of the bridgeEnv defining parameters.

    return lambda config: BridgeEnv(
        name = "CartpoleEnv", 
        ip = 'localhost',
        port = 10010,
        config = {
            "observation": obs_config, 
            "action": act_config
        },
        first_connection = False
    )
