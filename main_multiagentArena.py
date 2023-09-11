from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.envs import CartPole
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.bridge import Bridge

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

def get_ID(worker):
    return worker.env.get_ID()

def set_ID(worker):
    ID = worker.worker_index + 1
    worker.env.set_ID(ID)

def set_data(): 
    pass 


if __name__ == '__main__':
    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 2
    ))

    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=0)  
    
    algo = config.build(env = 'multiagents-arena')

    print(f"[ENV]:{algo.workers.local_worker().env} ")
    #print(f"[ADDING WORKERS]: {algo.workers.add_workers(1)}")
    print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
    print(f"[ENV ID]: {algo.workers.local_worker().env.ID}")
    
    #algo.workers.foreach_worker()
    
    NUM_ENVS = 2
    ip = 'localhost'
    port = 10011 
    
    env_config = MultiAgentArena.get_config()
    bridge = Bridge(env_config, ip, port)

    
    

    
    #assign IDs for each env.
    print(f"[ADDING WORKERS]: {algo.workers.add_workers(2)}")
    for i in range(algo.workers.num_remote_workers()):
        algo.workers.foreach_worker(set_ID)
    print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
    #algo.workers.add_workers(2)
    print(f"[ENV IDS]: {algo.workers.foreach_worker(get_ID)}")
    
    
    for i in range(2):
        print("training")
        result = algo.train()
        print(f"train {i}")
    print(result['episode_reward_mean'])

