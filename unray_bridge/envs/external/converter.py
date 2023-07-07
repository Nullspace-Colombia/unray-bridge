
from ray.rllib.env.external_env import ExternalEnv

def to_external_multiagent(objective_class):
    class NewClass(objective_class, ExternalEnv):
        def __init__(self): 
            pass 
    return NewClass
    
