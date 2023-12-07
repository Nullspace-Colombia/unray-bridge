from unray_bridge.envs.bridge.TCP_IP_Connector import ClientHandler
from unray_bridge.multiagents_config import MultiEnvCreator
from unray_bridge.envs.envs.MultiAgentArena import get_config
import numpy as np

import ray
from ray.rllib.algorithms.dqn import DQNConfig, DQNTFPolicy, DQNTorchPolicy
from ray.rllib.algorithms.ppo import (
    PPOConfig,
    PPOTF1Policy,
    PPOTF2Policy,
    PPOTorchPolicy,
)
from ray.rllib.examples.env.multi_agent import MultiAgentCartPole
from ray.tune.logger import pretty_print

from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.  envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.envs.spaces import BridgeSpaces

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

if __name__ == '__main__':


    
    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 1
    ))
    print("[ENV REGISTER SUCCESS]")
    #handler = bridge.get_client_handler()
    #data_handler = bridge.get_data_handler()
    

    ppo_config = PPOConfig()
    ppo_config = ppo_config.environment("multiagents-arena")
    ppo_config = ppo_config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    ppo_config = ppo_config.resources(num_gpus=0)  
    ppo_config = ppo_config.rollouts(num_rollout_workers=0)  
    
    #ppo = cppo_config.build(env = 'multiagents-arena')
    

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

    dqn_config = (
        DQNConfig()
        .environment("multiagents-arena")
        .training(
            model={"vf_share_layers": True},
            n_step=3,
            gamma=0.95,
        )
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
    )

    # Specify two policies, each with their own config created above
    # You can also have multiple policies per algorithm, but here we just
    # show one each for PPO and DQN.
    policies = {
        "ppo_policy": (
            select_policy("PPO", "tf"),
            BridgeSpaces.MultiDiscrete([64, 64]),
            BridgeSpaces.Discrete(4),
            ppo_config,
        ),
        "dqn_policy": (
            select_policy("DQN", "tf"),
            BridgeSpaces.MultiDiscrete([64, 64]),
            BridgeSpaces.Discrete(4),
            dqn_config,
        ),
    }

    def policy_mapping_fn(agent_id, episode, worker, **kwargs):
        if agent_id.endswith("1:1"):
            return "ppo_policy"
        else:
            return "dqn_policy"

    # Add multi-agent configuration options to both configs and build them.
    ppo_config.multi_agent(
        policies=policies,
        policy_mapping_fn=policy_mapping_fn,
        policies_to_train=["ppo_policy"],
    )
    ppo = ppo_config.build()

    dqn_config.multi_agent(
        policies=policies,
        policy_mapping_fn=policy_mapping_fn,
        policies_to_train=["dqn_policy"],
    )
    dqn = dqn_config.build()

    #sock = bridge.set_socket()
    #bridge.start(sock)
    #ppo.workers.local_worker().env.set_bridge(bridge)
    #dqn.workers.local_worker().env.set_bridge(bridge)
    # You should see both the printed X and Y approach 200 as this trains:
    # info:
    #   policy_reward_mean:
    #     dqn_policy: X
    #     ppo_policy: Y

    print("assign sock")
    ppo.workers.local_worker().env.connect_socket()
    s = ppo.workers.local_worker().env.get_socket()
    dqn.workers.local_worker().env.set_socket(s)

    for i in range(3):
        print("== Iteration", i, "==")

        # improve the DQN policy
        print("-- DQN --")
        result_dqn = dqn.train()
        print(pretty_print(result_dqn))

        # improve the PPO policy
        print("-- PPO --")
        result_ppo = ppo.train()
        print(pretty_print(result_ppo))