from unray_bridge.bridge import Bridge
from ray.tune.registry import register_env
     

from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.bridge import Bridge
from ray.rllib.algorithms.ppo import PPOConfig




class UnrayTrainer():
    def __init__(self):
        
        print("____________[TRAINER CREADO]___________-")
        
    def get_ID(self, worker):
        return worker.env.get_ID()

    def set_ID(self, worker):
        ID = worker.worker_index
        worker.env.set_ID(ID)

    def set_worker_bridge(self, worker):
        bridge_t = self.con_bridge
        print(f"[SETTING BRIDGE {id(bridge_t)} FOR WORKER : {worker.env.get_ID()}")
        
        worker.env.set_bridge(bridge_t)

    def configure_algo(self, config, env_t, env_name, num_workers):

        if config.num_rollout_workers > 0:
            n_envs = config.num_rollout_workers
            config.rollouts(num_rollout_workers=0) 
        else:
            n_envs = 1

        
        #self.con_bridge = Bridge(env_t.get_config(), n_envs, ip, port) # Bridge control 
        
        register_env(env_name, env_t.get_env(
            amount_of_envs= 1
        ))
        
    

        algo = config.build(env = env_name)
        algo.workers.add_workers(num_workers)

        print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
        
        algo.workers.foreach_worker(self.set_ID)

        if algo.workers.num_remote_workers() > 0:
            algo.workers.foreach_worker(lambda worker: worker.env.connect_socket(), local_worker=False)
            
        else:
            algo.workers.local_worker().env.connect_socket()

        return algo

