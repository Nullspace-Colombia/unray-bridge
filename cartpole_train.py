from unray_bridge.envs.envs import CartPole
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

import numpy as np

if __name__ == '__main__':
    register_env('cartpole', CartPole.get_env())

    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=1)

    algo = config.build(env = 'cartpole')
    for i in range(1):
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])