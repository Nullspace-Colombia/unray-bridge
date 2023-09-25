
from typing import Dict, Tuple
import argparse
import gymnasium as gym
import numpy as np
import os

import ray
from ray import air, tune
from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.env import BaseEnv
from ray.rllib.evaluation import Episode, RolloutWorker
from ray.rllib.policy import Policy
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.algorithms.pg.pg import PGConfig

class MyCallbacks(DefaultCallbacks):
    def on_episode_start(
        self,
        *,
        worker: RolloutWorker,
        base_env: BaseEnv,
        policies: Dict[str, Policy],
        episode: Episode,
        env_index: int,
        **kwargs
    ):
        # Make sure this episode has just been started (only initial obs
        # logged so far).
        # print(episode.length)
        assert episode.length == -1, (
            "ERROR: `on_episode_start()` callback should be called right "
            "after env reset!"
        )
        # Create lists to store angles in
        episode.user_data["y_direction_agent1"] = []
        episode.user_data["y_direction_agent2"] = []

        episode.hist_data["y_direction_agent1"] = []
        episode.hist_data["y_direction_agent2"] = []
    def on_episode_step(
        self,
        *,
        worker: RolloutWorker,
        base_env: BaseEnv,
        policies: Dict[str, Policy],
        episode: Episode,
        env_index: int,
        **kwargs
    ):
        # Make sure this episode is ongoing.
        assert episode.length > 0, (
            "ERROR: `on_episode_step()` callback should not be called right "
            "after env reset!"
        )
        y_pos = episode._last_infos['agent-1']['y']
        y_pos_2 = episode._last_infos['agent-2']['y']
        episode.user_data["y_direction_agent1"].append(y_pos)
        episode.user_data["y_direction_agent2"].append(y_pos_2)



    def on_episode_end(
        self,
        *,
        worker: RolloutWorker,
        base_env: BaseEnv,
        policies: Dict[str, Policy],
        episode: Episode,
        env_index: int,
        **kwargs
    ):
        # Check if there are multiple episodes in a batch, i.e.
        # "batch_mode": "truncate_episodes".

        y_pos1 = np.mean(np.array(episode.user_data["y_direction_agent1"]))
        y_pos2 = np.mean(np.array(episode.user_data["y_direction_agent2"]))

        y_pos = np.mean(np.array(episode.user_data["y_direction_agent1"]+episode.user_data["y_direction_agent2"]))
        episode.custom_metrics["y_direction_mean_agent1"] = y_pos1
        episode.custom_metrics["y_direction_mean_agent2"] = y_pos2

        episode.custom_metrics["y_direction_mean_both_agents"] = y_pos

        episode.hist_data["y_direction_agent1"] = episode.user_data["y_direction_agent1"]
        episode.hist_data["y_direction_agent2"] = episode.user_data["y_direction_agent2"]


    # def on_sample_end(self, *, worker: RolloutWorker, samples: SampleBatch, **kwargs):
        # We can also do our own sanity checks here.
        # assert samples.count == 200, "I was expecting 200 here!"

    def on_train_result(self, *, algorithm, result: dict, **kwargs):
        # you can mutate the result dict to add new fields to return
        result["callback_ok"] = True

        # Normally, RLlib would aggregate any custom metric into a mean, max and min
        # of the given metric.
        # For the sake of this example, we will instead compute the variance and mean
        # of the pole angle over the evaluation episodes.
        y_pos_1 = result["custom_metrics"]["y_direction_mean_agent1"]
        y_pos_2 = result["custom_metrics"]["y_direction_mean_agent2"]

        y_pos_ = result["custom_metrics"]["y_direction_mean_both_agents"]

        mean_1 = np.mean(y_pos_1)
        max_1 = np.max(y_pos_1)
        min_1 = np.min(y_pos_1)

        mean_2 = np.mean(y_pos_2)
        max_2 = np.max(y_pos_2)
        min_2 = np.min(y_pos_2)


        mean_ = np.mean(y_pos_)
        max_ = np.max(y_pos_)
        min_ = np.min(y_pos_)

        result["custom_metrics"]["y_direction_mean_agent1"] = mean_1
        result["custom_metrics"]["y_direction_mean_agent2"] = mean_2

        result["custom_metrics"]["y_direction_mean_both_agents"] = mean_

        result["custom_metrics"]["y_direction_max_agent1"] = max_1
        result["custom_metrics"]["y_direction_max_agent2"] = max_2

        result["custom_metrics"]["y_direction_max_both_agents"] = max_


        result["custom_metrics"]["y_direction_min_agent1"] = min_1
        result["custom_metrics"]["y_direction_min_agent2"] = min_2

        result["custom_metrics"]["y_direction_min_both_agents"] = min_


        # We are not interested in these original values
        # del result["custom_metrics"]["y_direction_mean_agent1"]
        # del result["custom_metrics"]["y_direction_mean_agent2"]
        
        # del result["custom_metrics"]["y_direction_mean_both_agents"]


