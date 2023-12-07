from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.envs import CartPole
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.unray_config import UnrayConfig
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

if __name__ == '__main__':
    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=0)  
    
    
    env_t = CartPole
    
    unray_config = UnrayConfig()
    algo = unray_config.configure_algo(config, env_t, "CartpoleEnv")

    for i in range(2):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])
