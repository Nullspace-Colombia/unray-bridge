
from unray_bridge.envs.envs import CartPole
from unray_bridge.envs.base_env import SingleAgentEnv
from unray_bridge.unray_config import UnrayConfig
from ray.rllib.algorithms.ppo import PPOConfig

if __name__ == '__main__':
      
    ppo_config = PPOConfig()

    ppo_config = ppo_config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    ppo_config = ppo_config.resources(num_gpus=0)  
    ppo_config = ppo_config.rollouts(num_rollout_workers=0)  

    env_config = CartPole.env_config

    cartpole = SingleAgentEnv(env_config, "CartpoleEnv")
    
    unray_config = UnrayConfig()

    algo = unray_config.configure_algo(ppo_config, cartpole)

    for i in range(2):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])
