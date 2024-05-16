from ray.rllib.algorithms.ppo import PPOConfig
from src.unray.envs.base_env import SingleAgentEnv
from src.unray.envs.spaces import BridgeSpaces
import numpy as np
from src.unray.unray_config import UnrayConfig
from ray.rllib.algorithms.algorithm import Algorithm
import matplotlib.pyplot as plt

high = np.array(
    [10000]*30,
    dtype=np.float32,
)

obs_config = {
    "space": BridgeSpaces.Box(-high, high),
    "description": "Observaciones"
}

act_config = {
    "space": BridgeSpaces.MultiDiscrete([3]),
    "description": "Acciones"
}

ppo_config = PPOConfig()

#ppo_config = ppo_config.training(gamma=0.9, lr=0.1, entropy_coeff=0.01, kl_coeff = 0.0)
ppo_config = ppo_config.resources(num_gpus=0)
ppo_config = ppo_config.rollouts(num_rollout_workers=0)



# Actions are : moving (forward, left, right, stop)
# All actions can be performed at the same time, and have state 0 and 1, for pressed and not pressed
env_config = {
    "observation": BridgeSpaces.Box(-high, high),
    "action":BridgeSpaces.MultiDiscrete([2,3])
}

# Create unray object
unray_config = UnrayConfig()

# Path
path = "C:/Users/Valentina/Documents/1_Universidad/AI/4_Tests/Soccer_Agent/R1" #"E:/Universidad/Codigo/Nullspace/UE5/AgentGardenProject/Models/soccer-v2"

# Create instance of single agent environment
env = SingleAgentEnv(env_config, "car_env")

# Create algo instance
algo = unray_config.configure_algo(ppo_config, env)

#algo.restore(path) #= Algorithm.from_checkpoint(path)
mean_ = []
min_ = []
max_ = []
episodes = []
# Train
for i in range (51):
    result = algo.train()
    print("Episodio:"f" '{i}'")
    """
    mean_.append(result['episode_reward_mean'])
    min_.append(result['episode_reward_min'])
    max_.append(result['episode_reward_max'])
    episodes.append(result['episodes_total'])
    print(result)
    print(len(min_))
    """
    if i % 5 == 0:

        save_result = algo.save(path)#("C:/Users/gonza/AppData/Local/Temp/tmp10hjh2wd")
        print("An Algorithm checkpoint has been created inside directory: "f"'{save_result}'.")
        """
        iters = [j for j in range(i+1)]
        plt.figure()
        plt.plot(iters, mean_, color='black', label='mean')
        plt.plot(iters, min_, ls='dashed', color='red', label='min')
        plt.plot(iters, max_, ls='dashed', color='blue', label='max')
        plt.xlabel('training steps')
        plt.title('PPO 15 Iteration training')
        plt.legend()
        plt.ylabel('reward')
        plt.savefig(f"Imagenes/iter_{i}")
        """



