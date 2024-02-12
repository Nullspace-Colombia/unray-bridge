from unray_bridge.envs.spaces import BridgeSpaces

env_config  = {
    "agent-1":{
        "observation": BridgeSpaces.MultiDiscrete([64, 64]),
        "action": BridgeSpaces.Discrete(4),
        "can_show": 1,
        "can_see": 2,                        
        "obs_order": {   
            "agent-1": [0], 
            "agent-2": [0]
        }
    }, 
    "agent-2":{
        "observation": BridgeSpaces.MultiDiscrete([64, 64]),
        "action": BridgeSpaces.Discrete(4),
        "can_show": 1,
        "can_see": 2,
        "obs_order": {
            "agent-2": [0], 
            "agent-1": [0]
        }
    },
    "agent-3":{
        "observation": BridgeSpaces.MultiDiscrete([64, 64]),
        "action": BridgeSpaces.Discrete(4),
        "can_show": 1,
        "can_see": 2,
        "obs_order": {
            "agent-3": [0], 
            "agent-4": [0]
        }
    },
    "agent-4":{
        "observation": BridgeSpaces.MultiDiscrete([64, 64]),
        "action": BridgeSpaces.Discrete(4),
        "can_show": 1,
        "can_see": 2,
        "obs_order": {
            "agent-4": [0], 
            "agent-3": [0]
        }
    }
}

