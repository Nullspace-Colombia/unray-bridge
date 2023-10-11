from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.envs import CartPole
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.bridge import Bridge
from unray_bridge.training import UnrayTrainer
import ray
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

if __name__ == '__main__':
    
    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=0)  
    
    
    env_t = MultiAgentArena
    
    trainer = UnrayTrainer()
    algo = trainer.configure_algo(config, env_t, 'multiagents-arena', num_workers= 4)
    for i in range(2):
        print(f"-------------------TRAINING ITERATION {algo.training_iteration}-------------------")
        result = algo.train()

        
    print(result['episode_reward_mean'])

"""
    ray.init()
    ip = 'localhost'
    port = 10011
    env_config = MultiAgentArena.get_config()
    i=0
    

    register_env('multiagents-arena', MultiAgentArena.get_env(
        amount_of_envs= 1
    ))

    config = PPOConfig()

    config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)  
    config = config.resources(num_gpus=0, num_cpus_per_trainer_worker=0.125)  
    config = config.rollouts(num_rollout_workers=0)  
    
    print(f"ROLLOUT: {config.num_rollout_workers}")
    #if config.num_rollout_workers > 0:
    #    n_envs = config.num_rollout_workers
    #    print(n_envs)
    #    config.rollouts(num_rollout_workers=0)
    n_envs = config.num_rollout_workers
    algo = config.build(env = 'multiagents-arena')
    #print(f"[ENV]:{algo.workers.local_worker().env} ")
    #print(f"[ADDING WORKERS]: {algo.workers.add_workers(3)}")
   # print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
    #print(f"[ENV ID]: {algo.workers.local_worker().env.ID}")
    
    #algo.workers.foreach_worker()
    #algo.workers._env_creator = MultiAgentArena.get_env(
    #    amount_of_envs= 1, env_bridge=con_bridge
    #)
    

    #print(f"[WORKER HOST]: {algo.workers.foreach_worker(get_worker_host)}")
    
    #print(f"[WORKER IDS]: {algo.workers.foreach_worker(print_IDS)}")
    print(f"[ADDING WORKERS]: {algo.workers.add_workers(4)}")
    #print(dir(algo.workers))
    algo.workers.foreach_worker(set_ID)
    #algo.workers.foreach_worker(lambda worker: print(worker.config))
    #print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
    #algo.workers.add_workers(2)
    #print(f"[ENV IDS]: {algo.workers.foreach_env(get_ID)}")
    #print(f"[ENV CREATOR] {algo.workers._env_creator}")
   # print("[SETTING BRIDGES]")
   # print(f"WORKERS: {algo.workers.remote_workers()}")
    
    #con_bridge = Bridge.remote(env_config, 2, ip, port) # Remote actor lass 
    #algo.workers.foreach_worker(set_bridge)
    #algo.workers.local_worker().env.connect_socket()
   # print(f"...............[FOREACHENV]: {algo.workers.foreach_env(lambda env: env.set_bridge(con_bridge))}.............")
    algo.workers.foreach_worker(lambda worker: worker.env.connect_socket(), local_worker=False)        
    
    #algo.workers.local_worker().env.set_bridge(con_bridge)
    #algo.workers.foreach_env(set_bridge)
    
    
    #sock = con_bridge.set_socket.remote()
    #print("UWUNT")
    #con_bridge.start.remote() # Begin Connection
    

    for i in range(2):
        print("training")
        result = algo.train()
        print(f"-----train {i}------")
    print(result['episode_reward_mean'])
"""
    



