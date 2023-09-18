from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.envs import CartPole
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.bridge import Bridge
from unray_bridge.training import UnrayTrainer

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

ip = 'localhost'
port = 10011
env_config = MultiAgentArena.get_config()
i=0
global con_bridge
con_bridge = Bridge(env_config, 2, ip, port)

def get_ID(env):
    return env.get_ID()

def set_ID(worker):
    ID = worker.worker_index + 1
    worker.env.set_ID(ID)
    
def set_data(): 
    pass 

def set_bridge(env):
    bridge_env_t = con_bridge
    print(f"[SETTING BRIDGE {id(bridge_env_t)} FOR ENV : {env.get_ID()}")
    env.set_bridge(bridge_env_t)

if __name__ == '__main__':

    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 1
    ))

    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=0)  
    
    print(f"ROLLOUT: {config.num_rollout_workers}")
    #if config.num_rollout_workers > 0:
    #    n_envs = config.num_rollout_workers
    #    print(n_envs)
    #    config.rollouts(num_rollout_workers=0)
    n_envs = config.num_rollout_workers
    algo = config.build(env = 'multiagents-arena')
    print(f"[ENV]:{algo.workers.local_worker().env} ")
   # print(f"[ADDING WORKERS]: {algo.workers.add_workers(2)}")
    print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
    #print(f"[ENV ID]: {algo.workers.local_worker().env.ID}")
    
    #algo.workers.foreach_worker()
    #algo.workers._env_creator = MultiAgentArena.get_env(
    #    amount_of_envs= 1, env_bridge=con_bridge
    #)
    

    
    #assign IDs for each env.
    #print(f"[ADDING WORKERS]: {algo.workers.add_workers(2)}")
    
    algo.workers.foreach_worker(set_ID)
    #print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
    #algo.workers.add_workers(2)
    print(f"[ENV IDS]: {algo.workers.foreach_env(get_ID)}")
    print(f"[ENV CREATOR] {algo.workers._env_creator}")
    print("[SETTING BRIDGES]")
    #algo.workers.foreach_worker(set_bridge, local_worker=False)
    
    algo.workers.foreach_env(set_bridge)
    con_bridge.set_socket()
    sock = con_bridge.get_socket()
        
    con_bridge.start(sock) # Begin Connection
    

    for i in range(2):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])

    
"""

    ip = 'localhost'
    port = 10011
    
    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=2)  
    
    
    env_t = MultiAgentArena
    
    trainer = UnrayTrainer()
    algo = trainer.configure_algo(config, env_t, 'multiagents-arena', ip, port)
    for i in range(2):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])
"""
