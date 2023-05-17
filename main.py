"""
Main.py 

    Options to select: 
        - singleangets: a simple example of BridgeConnection on a Cartpole 1D example
        - multiagents: a simple example of BridgeConnection on a 
"""

from tests.single_agents import single_agents
from tests.multiagents import multiagents
from argparse import ArgumentParser
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.envs.spaces import BridgeSpaces

import numpy as np



env_config = {
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

env = MultiAgentBridgeEnv(
    name = "multiagent-arena",
    ip = 'localhost',
    port = 10011, 
    config = env_config
)

# Actions test 
action = {
    'agent-1': np.array([0]),
    'agent-2': np.array([2])
}
action2 = {
    'agent-1': np.array([1]),
    'agent-2': np.array([0])
}
action3 = {
    'agent-1': np.array([3]),
    'agent-2': np.array([0])
}
action4 = {
    'agent-1': np.array([2]),
    'agent-2': np.array([1])
}

if __name__ == "__main__":
    env.step(action)
    print("------------------------------------------")
    env.step(action2)
    print("------------------------------------------")
    env.step(action3)
    print("------------------------------------------")
    env.step(action4)
    print("------------------------------------------")








    

    

    
    



