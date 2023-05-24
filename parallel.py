from unray_bridge.multiagents_config import MultiEnvCreator
from unray_bridge.envs.envs import MultiAgentArena

import pprint

config = MultiAgentArena.get_config()
MEC = MultiEnvCreator(config, amount_of_envs= 2)

multienv_dict = MEC.get_multienv_config_dict()
pprint.pprint(multienv_dict)
