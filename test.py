from unray_bridge.envs.envs import two_agents_test
from ray.rllib.algorithms.ppo import ppo
from ray.tune.registry import register_env
from ray.rllib.algorithms.registry import _get_algorithm_class
from ray.rllib.models.catalog import MODEL_DEFAULTS
import numpy as np 

env = two_agents_test.get_env(instance = True)
# Actions test 
# action = {
#     'agent-1': np.array([0,2,0,0]),
#     'agent-2': np.array([0,2,0,0]),
# }
obs,info = env.reset()
Algorithm = "PPO"
env_name = 'two_agent_test'
path_to_log = "./results/logs"
checkpoint_number = 36
register_env(env_name, two_agents_test.get_env())

config = ( _get_algorithm_class(Algorithm)
                .rollouts(num_rollout_workers=0))

algo = config.build(env = env_name)
if checkpoint_number:
    algo.restore(f'./results/checkpoint_{checkpoint_number:06}/')
if __name__ == "__main__":
    for i in range(10):
        action = algo.compute_single_action(obs)
        obs,reward,terminated,truncated,info = env.step(action)
        if terminated['__all__'] or truncated['__all__']:
            break
