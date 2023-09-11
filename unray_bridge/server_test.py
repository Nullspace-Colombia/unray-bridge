from envs.bridge.TCP_IP_Connector import ClientHandler
from bridge import Bridge
import numpy as np

from envs.envs import MultiAgentArena
from envs.bridge_env import MultiAgentBridgeEnv

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

if __name__ == '__main__':
    ip = 'localhost'
    port = 10011
    bridge = Bridge(ip, port)
    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 1, bridge = bridge
    ))
   
    #handler = bridge.get_client_handler()
    #data_handler = bridge.get_data_handler()

    bridge.start()
    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=0)  

    algo = config.build(env = 'multiagents-arena')

    for i in range(2):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])




