# Unray Bridge

Framework for communication between Unreal Engine and Python.

This repository contains all the files needed for usage in Python. To get the files needed for Unreal Engine, please check [Unreal Engine](#unreal-engine) section for details.

## Unreal Engine

Go to https://github.com/Nullspace-Colombia/Multiagents and clone the repo. This will provide you with all the files in the UE5 project.

### Engine Version

We are currently using Unreal Engine 5.1. We recommend using the same version to ensure project stability.

## CLI Unray 

## Getting Started
Clone the repo and install the given dependencies. This is just the python-side of the framework. Remember to create or to open a UE5 scene with the official unray-bridge blueprints.
```terminal
https://github.com/Nullspace-Colombia/unray-bridge.git  && cd unray-bridge 
 pip install -r requirements.txt
```
> We recommend conda for creating a virtualenv and installing the dependendencies. Currently, Ray is available in Python 3.10 or less, so we recommend creating a virtualenv with version 3.10.

### Running Examples

In your UE5 scene, start the MultiAgentArena_BP map. Once it is running, go to your terminal an inside the unray-bridge folder run:

```terminal
python main_local.py
```

If everything is correct, the agents will start to move. 

# RL Environment for simple training
## Single Agent
[In dev process]

## Multiagent 
In order to define a custom environment, you have to create an action and observation dictionary. This is called a *env_config* dict. 
```python3
# Define the env_config dict for each agent. 
env_config = {
  "agent-1": {
    "observation": <Space>,
    "action": <Space>
    }, 
  "agent-2": {
    "observation": <Space>,
    "action": <Space>
    }
    ...
```

Each Space is taken from BridgeSpace
```python
from unray_bridge.envs.spaces import BridgeSpaces 
```


This dictionary defines the independent spaces for each of the agents. Then, the environment is intantiated inherited from MultiAgentBridgeEnv from `unray_bridge`

```python3
from unray_bridge.envs.bridge_env import MultiAgentBridgeEnv
```

Contructor needs environment name, ip, port and the config.

```python


env = MultiAgentBridgeEnv(
    name = "multiagent-arena",
    ip = 'localhost',
    port = 10110, 
    config = env_config
)

```

### Multiagent Workflow 
As well as in the single-agent case, the environment dynamics are defined externally in the UE5 Scenario. The BridgeEnv lets RLlib comunicate with the enviornment via TPC/IP connection, sending the agent actions defined by ray algorithms and reciving the observation vectors from the environment for the trainer to train. The `MultiAgentBridgeEnv`creates the **connection_handler** that allow to maintain the socket communication. 

#### 1. How does the multiagent dictionaries are structured for sending to UE5 ? 
Suppose we have *n-agents* in the environment. Each of them with a given **a_i** action vector. This means that we have a total data of the sum of sizes for each action vector. Hence, stacking these vectors we got the final buffer that is send to the socket server from UE5.


### Multiagent Example: Multiagent-Arena
As a simple example we will build a Multiagent-Arena environment in UE5 an train it in ray using the unray-bridge framework. 

<p align="center"> 
<img width="70%" 
src="https://raw.githubusercontent.com/sven1977/rllib_tutorials/8be6297fe1012ae9643c0eec383484f0a3d9bf18/ray_summit_2021/images/environment.png"/> 
</p> 
Img taken from https://github.com/sven1977/rllib_tutorials/blob/main/ray_summit_2021/tutorial_notebook.ipynb

#### Understanding the environment
As a Unray-bridge philosophy first we have to break down what the environment need. We have to agents that move in the same scenario, given by a 8x8 square grid. They can only move one no-diagonal square for each episode. (The reward system is defined in the image). 

Hence we got: 
- **Agent 1 and 2 Observation:** MultiDiscrete([64])
- **Agent 1 and 2 Action:** Discrete([4])

Defining the env_config as follows: 

```python
  env_config  = {
    "agent-1":{
        "observation": BridgeSpaces.MultiDiscrete([64], [64]),
        "action": BridgeSpaces.Discrete(4),
    }, 
    "agent-2":{
        "observation": BridgeSpaces.MultiDiscrete([64], [64]),
        "action": BridgeSpaces.Discrete(4),
    }
}
```

Create the environment

```python
env = MultiAgentBridgeEnv(
    name = "multiagent-arena",
    ip = 'localhost',
    port = 10110, 
    config = env_config
)
```

### UE5 Environment

<p align="center">
  <img width="70%" src="https://github.com/mora200217/unray-bridge/blob/f/multiagent/assets/ue5-scene.png"
   ![Uploading multiagentArena.png…]()
 /> 
</p> 


# RL Environment for parallel training 
Central policy server is implemented


new parameters for multiagents lecture. 
* `can_see`: Number of supplied observation by the given agent. 
* `obs_order`: Order of observations for the given agent. Each observation could be from the agent and/or from other(s) agent(s)


