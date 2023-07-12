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
from unray_bridge.multiagents_config import MultiEnvCreator
from unray_bridge.envs.envs.MultiAgentArena import get_config


import numpy as np

single_env = get_config()
creator = MultiEnvCreator(single_env, amount_of_envs=1)
env_config = creator.get_multienv_config_dict()

env = MultiAgentBridgeEnv(
    name = "multiagent-arena",
    ip = 'localhost',
    port = 10011, 
    config = env_config
)

# Actions test 
action = {
    'agent-1:1': np.array([2]),
    'agent-2:1': np.array([0]),
    'agent-1:2': np.array([1]),
    'agent-2:2': np.array([3]),
}
action2 = {
    'agent-1:1': np.array([2]),
    'agent-2:1': np.array([0]),
    'agent-1:2': np.array([1]),
    'agent-2:2': np.array([3]),
}
action3 = {
    'agent-1:1': np.array([2]),
    'agent-2:1': np.array([3]),
    'agent-1:2': np.array([1]),
    'agent-2:2': np.array([3]),
}
action4 = {
    'agent-1': np.array([2]),
    'agent-2': np.array([2])
}

if __name__ == "__main__":
    env.step(action)
    print("------------------------------------------")
    env.step(action2)
    print("------------------------------------------")
    env.step(action3)
    print("------------------------------------------")







    

    

    
    



