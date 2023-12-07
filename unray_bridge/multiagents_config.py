# multiagent_config.py 

import numpy as np
import ray # temporal ? 


class MultiEnvCreator:
    """
        Multi Environment Creator
        ---
        Uses a single env multiagent configuration dict 
        and converts it into a multi env config. 
    """
    def __init__(self, config: dict, amount_of_envs = 1): 
        self.amount_of_envs = amount_of_envs # Amount of parallel environmentes 
        self.config = config 

    def validate_config(self): 
        """
            Validate Configuration
            ---
            Takes the single environment config dictionary and creates a multiple instance 
            stack for unreal 
        """
        pass 

    

    def get_amount_of_envs(self): 
        """
            get Amount of environments 
            ---
            @return self.envs - amount of environments created in parallel
        """
        return self.amount_of_envs
    
    def get_multienv_config_dict(self):
        """
            Get MultiEnvironment config dict
            ---
            Takes the single environment dictionary and replicates it into a multi-parallel 
            environments
        """
        new_dict = {}
        for i in range(self.amount_of_envs): 
            temp = {}
            for agent in list(self.config.keys()):
                temp[f"{agent}:{i + 1}"] = self.config[agent].copy()        
                temp[f"{agent}:{i + 1}"]['obs_order'] = self.update_obs_order(self.config[agent]['obs_order'].copy(), i + 1)

            new_dict.update(temp)
        return new_dict

    def update_obs_order(self, obs_order: dict, env_id: id): 
        temp = {}
        
        temp.update(obs_order)
        for key in list(temp.keys()):
            temp[f'{key}:{env_id}'] = temp[f'{key}']
            del temp[f'{key}']
        
        return temp
        
    
    def summary(self): 
        """
            Summary
            ---
            prints the main information of the Environment creator 
        """
        print("Multi Environment Creator Instance: ")
        print(f"\tAmount of environments: {self.get_amount_of_envs}")
        print(f"\tSummary of single env:")
        print("")