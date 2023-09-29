from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.envs import two_agents_test
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from ray.rllib.models.catalog import MODEL_DEFAULTS
from ray.rllib.models import ModelCatalog
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env
from ray.rllib.algorithms.registry import _get_algorithm_class
from custom.logger import custom_log_creator
from custom.plotter import plotter
from custom.customCallback import MyCallbacks
from ray import air, tune
import os
if __name__ == '__main__':

    Algorithm = "PPO"
    env_name = 'two_agent_test'
    path_to_log = "./results/logs"
    path_to_img = "./results/images"
    checkpoint_number = 44

    register_env(env_name, two_agents_test.get_env())
    default_model = MODEL_DEFAULTS
    default_model["fcnet_hiddens"] = [512,512]
    config = ( _get_algorithm_class(Algorithm)
              .get_default_config()
              .environment(clip_actions=True)
              .callbacks(MyCallbacks)
              .training(train_batch_size=512*3,lr=2e-5,vf_loss_coeff=0.4,
                            entropy_coeff=0.01,lambda_=0.9,num_sgd_iter=10,sgd_minibatch_size = 64,clip_param=0.25,gamma=0.99,
                             model=default_model)
                .debugging(seed=2,logger_creator=custom_log_creator(os.path.expanduser(path_to_log),f'{Algorithm}_{env_name}'))
                .resources(num_gpus=0,num_gpus_per_worker=0) 
                .reporting(keep_per_episode_custom_metrics=True)
                .rollouts(num_rollout_workers=1,rollout_fragment_length=512))

    algo = config.build(env = env_name)
    algo.get_policy().config['explore'] = False
    if checkpoint_number:
        algo.restore(f'./results/checkpoint_{checkpoint_number:06}/')

    for i in range(100):
        result = algo.train()
        algo.save('./results/')
        plotter(path_to_log,path_to_img)
    