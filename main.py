"""
    main.py 
"""
from unray_bridge.envs.envs import CartPole
from unray_bridge.envs.bridge_env import BridgeEnv

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

register_env('cartpole', CartPole.get_env())

config = PPOConfig()

config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
config = config.resources(num_gpus=0)  
config = config.rollouts(num_rollout_workers=1)  

algo = config.build(env = 'cartpole')
