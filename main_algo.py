from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
import matplotlib.pyplot as plt
from ray.rllib.algorithms.ppo import PPOConfig
# from ray.rllib.algorithms.ppo import PPOAgent
from ray.rllib.policy.policy import PolicySpec
from ray.rllib.examples.policy.random_policy import RandomPolicy
from ray.tune.registry import register_env
from ray.rllib.agents.ppo import PPOTrainer
from unray_bridge.envs.spaces import BridgeSpaces
from ray.rllib.algorithms.dqn import DQNConfig, DQNTFPolicy, DQNTorchPolicy
from ray.rllib.algorithms.ppo import (
    PPOConfig,
    PPOTF1Policy,
    PPOTF2Policy,
    PPOTorchPolicy,
)


def policy_mapping_fn(agent_id, episode, worker, **kwargs):
    if agent_id.endswith("1"):
        return "ppo"
    elif agent_id.endswith("2"):
        return "dqn"


def select_policy(algorithm, framework):
    if algorithm == "PPO":
        if framework == "torch":
            return PPOTorchPolicy
        elif framework == "tf":
            return PPOTF1Policy
        else:
            return PPOTF2Policy
    elif algorithm == "DQN":
        if framework == "torch":
            return DQNTorchPolicy
        else:
            return DQNTFPolicy
    else:
        raise ValueError("Unknown algorithm: ", algorithm)
    
if __name__ == '__main__':

    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 1
    ))

    ppo_config = (
        PPOConfig()
        .resources(num_gpus=0)  
        .rollouts(num_rollout_workers=0)
    )
    dqn_config = (
        DQNConfig()
        #.environment('multiagents-arena')
        .resources(num_gpus=0)  
        .rollouts(num_rollout_workers=0)
    )
    
    policies =  {
        "ppo": (select_policy("PPO","tf"), BridgeSpaces.MultiDiscrete([64, 64]), BridgeSpaces.Discrete(4), ppo_config),
        "dqn": (select_policy("DQN","tf"), BridgeSpaces.MultiDiscrete([64, 64]), BridgeSpaces.Discrete(4), dqn_config),
    }

    ppo_config.multi_agent(policies=policies, policy_mapping_fn = policy_mapping_fn, policies_to_train=["ppo"])
    ppo = ppo_config.build(env = 'multiagents-arena')

    dqn_config.multi_agent(policies=policies, policy_mapping_fn = policy_mapping_fn, policies_to_train=["dqn"])
    dqn = dqn_config.build(env = 'multiagents-arena')

    mean_ppo = []
    mean_dqn = []
    
    for i in range(1):
        print(f"training {i}")
        print(f"[ALGO]: PPO")
        results_ppo = ppo.train()
        mean_ppo.append(results_ppo['policy_reward_mean']['ppo'])
        print("------------------------------------------------")
        print(f"[ALGO]: DQN")
        results_dqn = dqn.train()
        mean_dqn.append(results_dqn['policy_reward_mean']['dqn'])

        #dqn.set_weights(ppo.get_weights(["ppo"]))
        #ppo.set_weights(dqn.get_weights(["dqn"]))

    print(f"[PPO: {results_ppo['policy_reward_mean']['ppo']}]")
    print(f"[DQN: {results_dqn['policy_reward_mean']['dqn']}]")

    iters = [i for i in range(2)]
    plt.plot(iters, mean_dqn, color="black", label='DQN')
    plt.plot(iters, mean_ppo, ls="dashed", color="red", label='PPO')
    plt.savefig('./training_algo.png')