""""
Main.py 

    Options to select: 
        - singleangets: a simple example of BridgeConnection on a Cartpole 1D example
        - multiagents: a simple example of BridgeConnection on a 
"""

from tests.single_agents import single_agents
from tests.multiagents import multiagents

from ray.rllib.env.policy_server_input import PolicyServerInput
from ray.rllib.examples.custom_metrics_and_callbacks import MyCallbacks
from ray.tune.logger import pretty_print
from ray.tune.registry import get_trainable_cls

from argparse import ArgumentParser

from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.envs.spaces import BridgeSpaces
from unray_bridge.policy_server import policy_server_input as psi

from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

import numpy as np
import ray


SERVER_ADDRESS = "localhost"
SERVER_BASE_PORT = 9900 



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
    port = 10010, 
    config = env_config
)

# Actions test 
action = {
    'agent-1': np.array([1]),
    'agent-2': np.array([-1])
}

ray.init()
    # `InputReader` generator (returns None if no input reader is needed on
    # the respective worker).
def _input(ioctx):
    # We are remote worker or we are local worker with num_workers=0:
    # Create a PolicyServerInput.
    if ioctx.worker_index > 0 or ioctx.worker.num_workers == 0:
        return PolicyServerInput(
            ioctx,
            SERVER_ADDRESS,
            SERVER_BASE_PORT
        )
    # No InputReader (PolicyServerInput) needed.
    else:
        return None
    
register_env('multiagents-arena', MultiAgentArena.get_env())

config = PPOConfig()

config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
config = config.resources(num_gpus=0)  
config = config.offline_data(input_=_input)
config = config.rollouts(num_rollout_workers=1, enable_connectors=False)  

algo = config.build(env = 'multiagents-arena')

for i in range(2):
    result = algo.train()
    print(f"train {i}")
print(result['episode_reward_mean'])    
