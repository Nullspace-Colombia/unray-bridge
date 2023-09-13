from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.envs import CartPole
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.bridge import Bridge
from unray_bridge.training import UnrayTrainer

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

def get_ID(worker):
    return worker.env.get_ID()

def set_ID(worker):
    ID = worker.worker_index + 1
    worker.env.set_ID(ID)

def set_data(): 
    pass 

def set_bridge(env):
    print(f"[SETTING BRIDGE {id(con_bridge)} FOR ENV : {env.get_ID()}")
    env.set_bridge(con_bridge)

if __name__ == '__main__':



    ip = 'localhost'
    port = 10011
    
    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=2)  
    
    
    env = MultiAgentArena
    trainer = UnrayTrainer()
    algo = trainer.train(config, env, 'multiagents-arena', ip, port)
    for i in range(2):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])
"""
    ip = 'localhost'
    port = 10011
    
    env_config = MultiAgentArena.get_config()
    con_bridge = Bridge(env_config, 2, ip, port)
    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 1
    ))

    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=0)  
    
    
    if config.num_rollout_workers > 0:
        n_envs = config.num_rollout_workers
        print(n_envs)
        config.rollouts(num_rollout_workers=0) 

    algo = config.build(env = 'multiagents-arena')
    print(f"[ENV]:{algo.workers.local_worker().env} ")
    #print(f"[ADDING WORKERS]: {algo.workers.add_workers(2)}")
    print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
    print(f"[ENV ID]: {algo.workers.local_worker().env.ID}")
    
    #algo.workers.foreach_worker()
    #algo.workers._env_creator = MultiAgentArena.get_env(
    #    amount_of_envs= 1, env_bridge=con_bridge
    #)
    

    
    #assign IDs for each env.
    print(f"[ADDING WORKERS]: {algo.workers.add_workers(2)}")
    
    algo.workers.foreach_worker(set_ID)
    print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
    #algo.workers.add_workers(2)
    print(f"[ENV IDS]: {algo.workers.foreach_worker(get_ID)}")
    print(f"[ENV CREATOR] {algo.workers._env_creator}")
    print("[SETTING BRIDGES]")
    #algo.workers.foreach_worker(set_bridge)
    algo.workers.foreach_env(set_bridge)
    
    

    sock = con_bridge.set_socket()
        
    con_bridge.start(sock) # Begin Connection

    for i in range(2):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])

    """
  
