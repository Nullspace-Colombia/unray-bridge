from unray_bridge.multiagents_config import MultiEnvCreator
from unray_bridge.envs.envs import MultiAgentArena

import pprint

config = MultiAgentArena.get_config()
MEC = MultiEnvCreator(config, amount_of_envs= 2)

# amount of agents 
amount_of_agents = config.keys().__len__
print(f"amount of agents: {amount_of_agents}")
print(f"amount of environments: {MEC.get_amount_of_envs()}")


multienv_dict = MEC.get_multienv_config_dict()
pprint.pprint(multienv_dict)
