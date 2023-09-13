from unray_bridge.envs.envs import MultiAgentArena
from unray_bridge.envs.envs import two_agents_test
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from ray.rllib.models.catalog import MODEL_DEFAULTS
from ray.rllib.models import ModelCatalog
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env
from ray.rllib.examples.models.fcnet_custom_pistonball import FullyConnectedNetworkCustom
if __name__ == '__main__':
    register_env('two_agent_test', two_agents_test.get_env())
    # ModelCatalog.register_custom_model("custom",FullyConnectedNetworkCustom)
    default_model = MODEL_DEFAULTS
    default_model["fcnet_hiddens"] = [256,256]
    # default_model["vf_share_layers"] = True
    default_model['fcnet_activation'] = "tanh"
    # default_model['free_log_std'] = True
    config = PPOConfig()  
    #  entropy_coeff_schedule=[[0,0.1],[5e7,0.001]],
    #  lr_schedule=[[0,5e-4],[1e8,2e-5]]
    config = config.environment(clip_actions=True)
    config = config.training(train_batch_size=512*4,lr=2e-5,vf_loss_coeff=0.25,
                            entropy_coeff=0.07,lambda_=0.9,num_sgd_iter=10,sgd_minibatch_size = 64,clip_param=0.3,gamma=0.99,
                             model=default_model)
                            # model={"fcnet_hiddens":[256,256],"vf_share_layers":True,"fcnet_activation":"tanh","free_log_std":True}
    # )
    # config = config.exploration(exploration_config={"type": "GaussianNoise","random_timesteps":0,"scale_timesteps":10e5,'final_scale':0.08,"stddev":1})
    config = config.debugging(seed=0)
    config = config.resources(num_gpus=0,num_gpus_per_worker=0)  
    config = config.rollouts(num_rollout_workers=1,rollout_fragment_length=512)
    # config = config.multi_agent(count_steps_by="agent_steps")
    algo = config.build(env = 'two_agent_test')

    for i in range(50):
        result = algo.train()
        algo.save('./results/')