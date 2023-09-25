from unray_bridge.multiagents_config import MultiEnvCreator
from unray_bridge.envs.envs import Two_Agent_Colaborative
from ray.rllib.algorithms.qmix import QMixConfig
from ray.tune.registry import register_env

#QMIX MAIN
if __name__ == '__main__':
    register_env('TwoAgentColaborative',  Two_Agent_Colaborative.get_env(amount_of_envs = 1))

    config = QMixConfig()  

    config = config.training(train_batch_size=512,lr=3e-5,gamma=0.99)
    config = config.exploration(exploration_config={"type": "StochasticSampling"})
    config = config.resources(num_gpus=0,num_gpus_per_worker=0)  
    config = config.rollouts(num_rollout_workers=1,rollout_fragment_length=256)

    algo = config.build(env = 'TwoAgentColaborative')
    iters = 50
    for i in range(iters):
        result = algo.train()
        checkpoint_dir = algo.save('./results/')