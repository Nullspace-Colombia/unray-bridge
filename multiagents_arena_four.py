"""
Main.py 

    Options to select: 
        - singleangets: a simple example of BridgeConnection on a Cartpole 1D example
        - multiagents: a simple example of BridgeConnection on a 
"""

from unray_bridge.envs.envs import MultiAgentArena_4
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

import numpy as np

if __name__ == "__main__":
    register_env('multiagents-arena', MultiAgentArena_4.get_env())

    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=1)

    algo = config.build(env = 'multiagents-arena')
    for i in range(1):
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])
