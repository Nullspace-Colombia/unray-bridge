from ray.rllib.algorithms.ppo import PPOConfig
from src.unray.envs.base_env import SingleAgentEnv
from src.unray.envs.spaces import BridgeSpaces
import numpy as np
from src.unray.unray_config import UnrayConfig
import matplotlib.pyplot as plt

high = np.array(
    [10000]*7,
    dtype=np.float32,
)

env_config = {
    "observation": BridgeSpaces.Box(-high, high),
    "action":BridgeSpaces.Discrete(2)
}

ppo_config = PPOConfig()

ppo_config = ppo_config.framework("torch")
ppo_config = ppo_config.resources(num_gpus=0)
ppo_config = ppo_config.rollouts(num_rollout_workers=0)

# Create unray object
unray_config = UnrayConfig()

# Create instance of single agent environment
env = SingleAgentEnv(env_config, "car_env")

# Create algo instance
algo = unray_config.configure_algo(ppo_config, env)

mean_ = []
min_= []
max_= []
episodes = []

#algo.restore(path)
for i in range (25):
    result = algo.train()
    print(f"Training {i}")
    mean_.append(result['episode_reward_mean'])
    min_.append(result['episode_reward_min'])
    max_.append(result['episode_reward_max'])
    episodes.append(result['episodes_total'])

print(result)
iters = [i for i in range(25)]
plt.plot(iters,mean_,color = 'black',label='mean')
plt.plot(iters,min_,ls='dashed',color='red',label='min')
plt.plot(iters,max_,ls='dashed',color='blue',label='max')
plt.xlabel('training steps')
plt.title('PPO 25 Iteration training - LLM Reward')
plt.legend()
plt.ylabel('reward')
plt.savefig('training_LLM.png')