from unray_bridge.envs.spaces import BridgeSpaces
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
from unray_bridge.multiagents_config import MultiEnvCreator
import numpy as np

high = np.array(
            [10000]*8,
            dtype=np.float32,
        )
agents = [f"agent-{i+1}" for i in range(20)]

env_config = {agents[j]: {
              "observation":BridgeSpaces.Box(-high, high),
              "action": BridgeSpaces.Box(-1,1),
              "can_show": 2, # Amount of observations int obs stack
              "can_see": 8, # Amount of observations required in training
              "obs_order": {agents[j]:[0,1]}}
              for j in range(20)}

for j in range(20):
  env_config[agents[j]]['obs_order'].update({k:[] for k in agents[0:j]+agents[j+1:] })
  if j ==0:
    env_config[agents[j]]["can_see"] = 8 
    env_config[agents[j]]["can_show"] = 7  
    env_config[agents[j]]['obs_order'][agents[j]]=[0,1,2,3,4,5,6]
    env_config[agents[j]]['obs_order'][agents[j+1]]=[1]
  elif j ==19:
    env_config[agents[j]]["can_see"] = 8
    env_config[agents[j]]["can_show"] = 8   
    env_config[agents[j]]['obs_order'][agents[j]]=[0,1,2,3,4,5,6,7]
  else:
    env_config[agents[j]]['obs_order'][agents[0]] = [2,3,4,5]
    env_config[agents[j]]['obs_order'][agents[j-1]]+=[1]
    env_config[agents[j]]['obs_order'][agents[j+1]]=[1]
def get_config():
    return env_config

def get_env(_ip = 'localhost', _port=10010, instance = False, amount_of_envs = 1):
    if amount_of_envs > 1:
        MCE = MultiEnvCreator(get_config(), amount_of_envs= amount_of_envs )
        env_config = MCE.get_multienv_config_dict()
    else:
        env_config = get_config()

    if instance:
        return MultiAgentBridgeEnv(
        name = "PistonBall", 
        ip = _ip,
        port = _port,
        config = env_config,
        first_connection = False
    )
    return lambda config: MultiAgentBridgeEnv(
        name = "PistonBall", 
        ip = _ip,
        port = _port,
        config = env_config,
        first_connection = False
    )



