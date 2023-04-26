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

import numpy as np
# Constants 
# _OPTION = "multiagents"

# # Parser 
# parser = ArgumentParser()

# parser.add_argument(
#     "test",
# )

# if __name__ == "__main__": 
#     # gui.print_title()
#     if _OPTION == "single-agents":
#         print("Single agents | CartPoleV1")
#         single_agents()
#     elif _OPTION == "multiagents": 
#         multiagents()
#     else: 
#         print("only options are ['single-agents', 'multiagents']")
#         print("*please select a valid option from the list above")  
#         print("")
from unray_bridge.envs.spaces import BridgeSpaces


env_config  = {
    "agent-1":{
        "observation": BridgeSpaces.MultiDiscrete([64, 64]),
        "action": BridgeSpaces.Discrete(4),
    }, 
    "agent-2":{
        "observation": BridgeSpaces.MultiDiscrete([64, 64]),
        "action": BridgeSpaces.Discrete(4),
    }
}

env = MultiAgentBridgeEnv(
    name = "multiagent-arena",
    ip = 'localhost',
    port = 10110, 
    config = env_config
)

# Actions test 
action = {
    'agent-1': np.array([2]),
    'agent-2': np.array([1])
}

env.step(action)



