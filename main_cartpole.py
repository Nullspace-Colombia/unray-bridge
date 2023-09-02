from unray_bridge.envs.envs import two_agents_test

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

if __name__ == '__main__':
    register_env('TwoAgentColab', two_agents_test.get_env())

    config = PPOConfig()

    config = config.training()  
    config = config.resources(num_gpus=0)  
    config = config.rollouts(num_rollout_workers=0)  

    algo = config.build(env = 'TwoAgentColab')
    # algo.restore('./results/checkpoint_000037')
    for i in range(50):
        result = algo.train()
        algo.save('./results')
