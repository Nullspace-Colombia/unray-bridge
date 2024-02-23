# About Unray

Framework for communication between Unreal Engine and Python.

This repository contains all the files needed for usage in Python.

# Unreal Engine

### Engine Version

We are currently using Unreal Engine 5.1. We recommend using the same version to ensure project stability.

### Plugin Version

We currently have version 1.1 of the plugin. If you still have version 1.0 please update to this new version.

Mistakes regarding the parallel training of Single Agent Environment have been fixed. 

## Project Files

In the Maps folder you'll find some examples to run:

![Maps](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/dd5a8093-a6da-4c88-8731-1b993d9faec8)


## Custom Envs

To create a custom env in Unreal Engine, first create your Agent Blueprint. 

You can create your agent based on the parent class of your choice. Once you create the blueprint, go to the ```Class Settings``` section.

![Class_Settings](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/10695530-d6b3-4b1e-a1a0-014e4a7b7008)

In the details panel, find the ```Interfaces``` section:

![Details_Panel](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/8ac78280-956a-4eff-9d62-5747af6514eb)

In the ```Implemented Interfaces``` subsection, click the ```Add``` button and search for "BI_Agent".

![Interface](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/ff7fb690-e23b-4c7a-9170-0fc0ff81d382)

![BI_Agent](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/ab14faee-521b-4f20-a7c4-c99736ea4ee9)

![Interface_Result](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/e0424945-374d-4786-8c1f-5db6ae402584)

Once you do this, in the blueprint functions, you'll now have these functions:

![Override_Functions](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/8709d437-53fb-4371-88bb-e4f8141d11a5)

You have to implement these functions according to your enviornment. 

| Function | Description |
|--------|---------|
|```Get Reward```| Agent Reward | 
| ```Is Done```| Function to specify the way the agent finishes the environment |
| ```Reset```  |  Reset the agent. ```Create Actor``` -> True if you want to destroy the actor and spawn it again in a new place. |
| ```Get State``` | Get agent observations |
| ```Step``` | What the agent does in each step |

When you've implemented all these functions and you want to try your environment, you'll have to add a **Connector** to your map.

In the Blueprints folder, you'll find the connectors for both single agent envs and multiagent envs:

![Connectors](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/d7e4c7f1-f234-4b0d-88bd-e2d2fcc188b4)

### Single Agent Environments

If your environment is a single agent env, place a ```Connector_SA``` instance in your map. Once you do, you can select it and in the details panel you'll find the Default section. There, you'll find an Actor Agent variable, assign your agent to this variable. 


### MultiAgent Environments

If your environment is a multiagent env, you'll need to place a ```Connector_MA``` instance in your map. Once you do, you can select it and in the details panel you'll find the Default section. There, you'll find an array called Actor Agents. 

![ConnectorMA_Panel](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/5989c256-024c-4386-b8c5-a585d493488f)

To ensure the framework can recognise all the agents in your environment, add each agent to the array. 

Remember that for each agent in your env, you'll have to implement the Reward, Done, Reset, Get State and Step functions.



## Parallel Trainning

If you want to train several envs at the same time, we recommend you create your env as a Blueprint. 

### Single Agent Environments

In the Blueprints folder you'll find a ```SingleAgent_Env``` Blueprint.

You can create your env with this Blueprint as a parent Class.

In the Viewport of your env blueprint class, drag one of the ```Conector_SA``` from the Content Drawer and place it where you want. 

In the Event Graph of your env blueprint class, you'll have to do a few things to configure your env. 

Set your Agent to the ```Agent``` variable that bellongs to the ```SingleAgent_Env``` class and add the following functions in your env class event graph:

![SingleAgentEnv](https://github.com/Nullspace-Colombia/unray-bridge/assets/55969494/1f9a498d-af3c-4076-b890-6e42bc67097c)

### MultiAgent Environments

In the Blueprints folder you'll find a ```MultiAgent_Env``` Blueprint.

![Env](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/36be5b8e-78bb-4144-8882-b9e6b8d154e1)

You can create your env with this Blueprint as a parent Class.

In the Viewport of your env blueprint class, drag one of the ```Conector_SA``` from the Content Drawer and place it where you want. 

In the Event Graph of your env blueprint class, you'll have to do a few things to configure your env. 

First, each env you create will have an ID (which defaults to 1). You can either set this parameter in the Details pannel of your map or create a function to set it automatically.

Then, you need to add the agents in your env to an ```Agents``` array, which belongs to the ```MultiAgent_Env``` class. To do so, simply search for the ```Get Agents``` function and add each of your agents to this array. For example, in the MultiAgent Arena map it looks like this:

![AddAgents](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/7f6670bc-7bc0-4163-b854-652bcefdb9b3)

Finally, you'll have to add the following functions to your env class: 

![MultiAgentEnv](https://github.com/Nullspace-Colombia/Multiagents/assets/55969494/ba178e2f-6dc9-4fd0-9d7a-61f71d9e06ef)

This is to set the agents and set the ports in which the communication is going to happen.


# UNRAY Bridge
Clone the repo and install the given dependencies. This is just the python-side of the framework. Remember to create or to open a UE5 scene with the official unray-bridge blueprints.
```terminal
https://github.com/Nullspace-Colombia/unray-bridge.git  && cd unray-bridge 
 pip install -r requirements.txt
```
We recommend conda for creating a virtualenv and installing the dependendencies. Currently, Ray is available in Python 3.10 or less, so we recommend creating a virtualenv with version 3.10.

### Running Examples
There are currently two examples ready for you to run.

#### Cartpole

![Cartpole](https://github.com/Nullspace-Colombia/unray-bridge/assets/55969494/801fcc65-ab24-41e2-9d20-6ef4fa186fda)

In Unreal Engine, go to the maps folder and start the Cartpole map. Once it is running, go to your terminal an inside the unray-bridge folder run:

```terminal
python main_cartpole.py
```

If everything is correct, the cartpole will start to move. 

#### MultiAgent Arena

![MultiAgentArena_S](https://github.com/Nullspace-Colombia/unray-bridge/assets/55969494/3eddf96d-8d72-4838-a7ca-ffa71bbe6832)


In this env, you have two agents competing in a single env. 

In Unreal Engine, go to the maps folder and start the MultiAgentArena map. Once it is running, go to your terminal an inside the unray-bridge folder run:

```terminal
python main_multiagentArena.py
```

If everything is correct, the agents will start to move. 

### MultiAgent Arena Parallel Trainning

![MultiAgentArena](https://github.com/Nullspace-Colombia/unray-bridge/assets/55969494/1940d152-716d-4a2c-98f5-4383228bf384)

In Unreal Engine, go to the maps folder and start the MultiAgentArena_BP map. Once it is running, go to your terminal an inside the unray-bridge folder run:

```terminal
python parallel_multiagentArena.py
```

If everything is correct, the four envs will start to move. 


# RL Environment for simple training
NOTE: We recommend reading this documentation with a basic RLlib knowledge. You can read the RLlib documentation here: https://docs.ray.io/en/latest/rllib/index.html

## Single Agent
In order to define a custom environment, you have to create an action and observation dictionary. This is called a *env_config* dict. 
```python3
# Define the env_config dict for each agent. 
env_config = {
  "observation": <Space>,
  "action" :<Space>
}
```

Each Space is taken from BridgeSpace
```python
from unray_bridge.envs.spaces import BridgeSpaces 
```
Once you have your *env_config* dict ready, we'll create the ```Unray``` object, which will allow us to train our environment with Unray. 

```
#Create Unray object

unray_config = UnrayConfig()
```

This will allow us to configure our algorithm to be ready for the communication with Unreal Eninge.

Next, we'll need to create an instance of a Single Agent Environment, which takes our *env_config* as an argument and a name for our env:

```
#Create Instance of Single Agent Environment

env = SingleAgentEnv(env_config, 'env_name')
```

Now, we can use unray without problem. After creating the config for our algorithm (like PPO) using RLlib, we'll create our algorithm instance using the ```configure_algo``` function from our Unray object, which takes in two arguments: our algorithm config and the single agent environment instance

```
#Create Algo Instance
algo = unray_config.configure_algo(algo_config, env)
```

Now, Unray is ready to train your Single Agent Environment.

### Single Agent Example: Cartpole

We'll take the classic cartpole example to start with unray.

First, let's create the action and observation dictionary. We are using the cartpole problem definition used in Gymnausium: https://gymnasium.farama.org/environments/classic_control/cart_pole/

```python3
high = np.array(
                [
                    1000,
                    np.finfo(np.float32).max,
                    140,
                    np.finfo(np.float32).max,
                ],
                dtype=np.float32,
            )

## Configurations Dictionaries
# Define all the observation/actions spaces to be used in the Custom environment 
# BridgeSpaces area based from gym.spaces. Check the docs for more information on how to use then. 

# for this example we are using a a BoxSpace for our observations and a 
# Discrete space for our action space.


env_config = {
        "observation": BridgeSpaces.Box(-high, high), 
            "action": BridgeSpaces.Discrete(2)
        }
```


## Multiagent 
In order to define a custom environment, you have to create an action and observation dictionary. This is called a *env_config* dict. 
```python3
# Define the env_config dict for each agent. 
env_config = {
  "agent-1": {
    "observation": <Space>,
    "action": <Space>,
    "can_show": int,
    "can_see": int,
    "obs_order":{
         "agent-1": i,
         "agent-2": j,
         ....
      }
    }, 
  "agent-2": {
    "observation": <Space>,
    "action": <Space>,
    "can_show": int,
    "can_see": int,
    "obs_order":{
         "agent-1": i,
         "agent-2": j,
         ....
      }
    }, 
    ...
```

Each Space is taken from BridgeSpace
```python
from unray_bridge.envs.spaces import BridgeSpaces 
```
This dictionary defines the independent spaces for each of the agents. You will also notice that for each agent there are three new parameters: ```can_show```, ```can_see``` and ```obs_order```. This parameters will help us define how each agent will see the other agents in the environment.

| Parameter | Description |
|--------|---------|
|```can_show```| The observations which will be available to other agents in the environment | 
| ```can_see```| How many observations can this agent see from other agents |
| ```obs_order```  | The order of the observations this agent can see from the other agents |


Once you have your *env_config* dict ready, we'll create the ```Unray``` object, which will allow us to train our environment with Unray. 

```
#Create Unray object

unray_config = UnrayConfig()
```

This will allow us to configure our algorithm to be ready for the communication with Unreal Eninge.

Next, we'll need to create an instance of a MultiAgent Environment, which takes our *env_config* as an argument and a name for our env:

```
#Create Instance of MultiAgent Environment

env = MultiAgentEnv(env_config, 'env_name')
```

Now, we can use unray without problem. After creating the config for our algorithm (like PPO), we'll create our algorithm instance using the ```configure_algo``` function from our Unray object, which takes in two arguments: our algorithm config and the single agent environment instance

```
#Create Algo Instance
algo = unray_config.configure_algo(algo_config, env)
```

Now, Unray is ready to train your Single Agent Environment.


### Multiagent Workflow 
As well as in the single-agent case, the environment dynamics are defined externally in the UE5 Scenario. Unray lets RLlib comunicate with the enviornment via TPC/IP connection, sending the agent actions defined by ray algorithms and reciving the observation vectors from the environment for the trainer to train. 

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
As a Unray-bridge philosophy first we have to break down what the environment need. We have two agents that move in the same scenario, given by a 8x8 square grid. They can only move one no-diagonal square for each episode. (The reward system is defined in the image). 

Hence we got: 
- **Agent 1 and 2 Observation:** MultiDiscrete([64])
- **Agent 1 and 2 Action:** Discrete([4])

Defining the env_config as follows: 

```python
env_config  = {
        "agent-1":{
            "observation": BridgeSpaces.MultiDiscrete([64, 64]),
            "action": BridgeSpaces.Discrete(4),
            "can_show": 1, # Amount of observations int obs stack
            "can_see": 2, # Amount of observations required in training 
            "obs_order": {   
                "agent-1": [0], 
                "agent-2": [0]
            }
        }, 
        "agent-2":{
            "observation": BridgeSpaces.MultiDiscrete([64, 64]),
            "action": BridgeSpaces.Discrete(4),
            "can_show": 1, # Amount of observations int obs stack
            "can_see": 2,
            "obs_order": {
                "agent-2": [0], 
                "agent-1": [0]
            }
        }
    }
```

Configure the environment

```python
    
    unray_config = UnrayConfig()
    arena = MultiAgentEnv(env_config, "multiagents-arena")
    algo = unray_config.configure_algo(ppo_config, arena)
```




