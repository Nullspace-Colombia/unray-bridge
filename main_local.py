from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
import matplotlib.pyplot as plt
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env
    
if __name__ == '__main__':

    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 2
    ))

    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=0)  

    algo = config.build(env = 'multiagents-arena')
    mean_ = []
    min_= []
    max_= []
    episodes = []
    for i in range(10):
        print("training")
        result = algo.train()
        mean_.append(result['episode_reward_mean'])
        min_.append(result['episode_reward_min'])
        max_.append(result['episode_reward_max'])
        episodes.append(result['episodes_total'])
    print(mean_)
    iters = [i for i in range(10)]
    plt.plot(iters,mean_,color = 'black',label='mean')
    plt.plot(iters,min_,ls='dashed',color='red',label='min')
    plt.plot(iters,max_,ls='dashed',color='blue',label='max')
    plt.xlabel('training steps')
    plt.title('PPO 10 iteration training')
    plt.legend()
    plt.ylabel('reward')
    plt.savefig('./training_10.png')
    

