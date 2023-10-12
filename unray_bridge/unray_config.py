
from ray.tune.registry import register_env
     

from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv

from ray.rllib.algorithms.ppo import PPOConfig




class UnrayConfig():
    def __init__(self):
        
        pass
        
    def get_ID(self, worker):
        return worker.env.get_ID()

    def set_ID(self, worker):
        ID = worker.worker_index
        worker.env.set_ID(ID)


    def configure_algo(self, config, env_t, env_name):

        if config.num_rollout_workers > 0:
            num_workers = config.num_rollout_workers
            config.rollouts(num_rollout_workers=0)
        else:
            num_workers = 0
        
        
        register_env(env_name, env_t.get_env(
            amount_of_envs= 1
        ))
        
    
        print("ENV REGISTERED")
        algo = config.build(env = env_name)


        if num_workers > 0:
            algo.workers.add_workers(num_workers)

            print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
            algo.workers.foreach_worker(self.set_ID)
            algo.workers.foreach_worker(lambda worker: worker.env.connect_socket(), local_worker=False)
            
        else:
            algo.workers.local_worker().env.connect_socket()

        return algo

