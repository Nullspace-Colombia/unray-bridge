from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
import matplotlib.pyplot as plt
from ray.rllib.algorithms.ppo import PPOConfig
#from ray.rllib.algorithms.ppo import PPOAgent
from ray.rllib.policy.policy import PolicySpec
from ray.rllib.examples.policy.random_policy import RandomPolicy
from ray.tune.registry import register_env
from ray.rllib.agents.ppo import PPOTrainer
from unray_bridge.envs.spaces import BridgeSpaces

def policy_mapping_fn(agent_id, episode, worker, **kwargs):
    if agent_id.endswith(":1"):
        return "arena_1"
    elif agent_id.endswith(":2"):
        return "arena_2"
    
if __name__ == '__main__':

    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 2
    ))

    policies =  {
        "arena_1": (None, BridgeSpaces.MultiDiscrete([64, 64]), BridgeSpaces.Discrete(4), {"lr": 0.01}),
        "arena_2": (None, BridgeSpaces.MultiDiscrete([64, 64]), BridgeSpaces.Discrete(4), {"lr": 0.002}),
    }
    
    config = (
        PPOConfig()
        .multi_agent(policies=policies, policy_mapping_fn = policy_mapping_fn)
        .resources(num_gpus=0)  
        .rollouts(num_rollout_workers=0)
    )
    
    algo = config.build(env = 'multiagents-arena')
    for i in range(10):
        print("training")
        results = algo.train()
    print(results['policy_reward_mean']['arena_1'])
    print(results['policy_reward_mean']['arena_2'])


"""
    algo = PPOTrainer(config = config)
    for i in range(1):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])

    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=0)  

    algo = config.build(env = 'multiagents-arena')
"""


