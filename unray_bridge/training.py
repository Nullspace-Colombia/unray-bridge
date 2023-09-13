from unray_bridge.bridge import Bridge
from ray.tune.registry import register_env
     

from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.bridge import Bridge
from ray.rllib.algorithms.ppo import PPOConfig

class UnrayTrainer():
    def __init__(self):
        self.con_bridge = None
        print("____________[TRAINER CREADO]___________-")
        
    def get_ID(self, worker):
        return worker.env.get_ID()

    def set_ID(self, worker):
        ID = worker.worker_index + 1
        worker.env.set_ID(ID)

    def set_bridge(self, worker):
        bridge_t = self.con_bridge
        print(f"[SETTING BRIDGE {id(bridge_t)} FOR WORKER : {worker.env.get_ID()}")
        
        worker.env.set_bridge(bridge_t)

    def train(self, config, env, env_name, ip = 'localhost', port = 10011):

        if config.num_rollout_workers > 0:
            n_workers = config.num_rollout_workers
            n_envs = n_workers
            print(f"[N_ENVS]:{n_envs}" )
            config.rollouts(num_rollout_workers=0) 
        else:
            n_envs = 1
        print("[Bridge] Starting instance...")

        
        self.con_bridge = Bridge(env.get_config(), n_envs, ip, port) # Bridge control 
        
        register_env(env_name, env.get_env(
            amount_of_envs= 1
        ))
        print("[Bridge] Created!")

        print("[STARTING BRIDGE]")
        
    

        algo = config.build(env = env_name)
        print(f"[N_ENVS]: {n_envs}")
        algo.workers.add_workers(n_workers)

        print(f"[NUM WORKERS]: {algo.workers.num_remote_workers()}")
     

        print("SETTING IDS")
        
        algo.workers.foreach_worker(self.set_ID)

        print(f"[ENV IDS]: {algo.workers.foreach_worker(self.get_ID)}")

        
        print("SETTING BRIDGE")
        if algo.workers.num_remote_workers() > 0:
            print("[SETTING BRIDGE FOR WORKERS]")
            print(f".................[BRIDGE]: {id(self.con_bridge)}.............")
            algo.workers.foreach_worker(self.set_bridge)
            
        else:
            algo.workers.local_worker().env.set_bridge(self.con_bridge)
        
        print(f"[NUM WORKERS]: {algo.workers.num_healthy_workers()}")
        sock = self.con_bridge.set_socket()
        
        self.con_bridge.start(sock) # Begin Connection
        return algo

