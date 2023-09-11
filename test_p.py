from unray_bridge.envs.bridge.TCP_IP_Connector import ClientHandler
from unray_bridge.bridge import Bridge
from unray_bridge.multiagents_config import MultiEnvCreator
from unray_bridge.envs.envs.MultiAgentArena import get_config
import numpy as np

from ray.rllib.algorithms.dqn.dqn import DQNConfig
from ray.rllib.algorithms.dqn.dqn_tf_policy import DQNTFPolicy
from ray.rllib.algorithms.dqn.dqn_torch_policy import DQNTorchPolicy
from ray.rllib.algorithms.ppo.ppo import PPOConfig
from ray.rllib.algorithms.ppo.ppo_tf_policy import PPOTF1Policy
from ray.rllib.algorithms.ppo.ppo_torch_policy import PPOTorchPolicy

from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.  envs.bridge_env import MultiAgentBridgeEnv

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

def set_bridge(bridge_env):
        bridge_env.set_bridge(bridge)

if __name__ == '__main__':
    ip = 'localhost'
    port = 10011
    
    env_config = MultiAgentArena.get_config()
    bridge = Bridge(env_config, ip, port)
    print("[BRIDGE STARTED]")
    #"""
    
    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 1, bridge=bridge
    ))
    print("[ENV REGISTER SUCCESS]")
    #handler = bridge.get_client_handler()
    #data_handler = bridge.get_data_handler()
    

    
    
    config_ppo = PPOConfig()

    config_ppo = config_ppo.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config_ppo = config_ppo.resources(num_gpus=0)  
    config_ppo = config_ppo.rollouts(num_rollout_workers=0)  
    
    algo = config_ppo.build(env = 'multiagents-arena')
    sock = bridge.set_socket()
    bridge.start(sock)
    algo.workers.local_worker().env.set_bridge(bridge)
    algo.workers.local_worker().env.set_ID(1)
    
    #if algo.workers.local_worker().env.amount_of_envs:
        
             

    
    for i in range(2):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])

"""
    single_env = get_config()
    creator = MultiEnvCreator(single_env, amount_of_envs=1)
    env_config = creator.get_multienv_config_dict()

    env = MultiAgentBridgeEnv(
        name = "multiagent-arena",
        ip = 'localhost',
        port = 10011, 
        config = env_config,
        bridge=bridge
    )

    # Actions test 
    action = {
        'agent-1:1': 2,
        'agent-2:1': 3
    }
    action2 = {
        'agent-1:1': 2,
        'agent-2:1': 3
    }
    action3 = {
        'agent-1:1': 4,
        'agent-2:1': 0
    }
    action4 = {
        'agent-1': 4,
        'agent-2': 0
    }

    if __name__ == "__main__":
        env.step(action)
        print("------------------------------------------")
        env.step(action)
        print("------------------------------------------")
        env.step(action)
        print("------------------------------------------")
"""

    
    
    

    


    
        

