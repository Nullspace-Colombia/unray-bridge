
import argparse

from ray.rllib.env.policy_client import PolicyClient

from unray_bridge.envs.envs import MultiAgentArena


SERVER_ADDRESS = "localhost"
SERVER_PORT = 9900

parser = argparse.ArgumentParser()
parser.add_argument(
    "--game",
    type=str,
    default=None,
    help="The game executable to run as RL env. If not provided, uses local ",
)
parser.add_argument(
    "--horizon",
    type=int,
    default=200,
    help="The max. number of `step()`s for any episode (per agent) before "
    "it'll be reset again automatically.",
)
parser.add_argument(
    "--server",
    type=str,
    default=SERVER_ADDRESS,
    help="The Policy server's address to connect to from this client.",
)
parser.add_argument(
    "--port", type=int, default=SERVER_PORT, help="The port to use (on --server)."
)
parser.add_argument(
    "--no-train",
    action="store_true",
    help="Whether to disable training (on the server side).",
)
parser.add_argument(
    "--inference-mode",
    type=str,
    default="local",
    choices=["local", "remote"],
    help="Whether to compute actions `local`ly or `remote`ly. Note that "
    "`local` is much faster b/c observations/actions do not have to be "
    "sent via the network.",
)
parser.add_argument(
    "--update-interval-local-mode",
    type=float,
    default=10.0,
    help="For `inference-mode=local`, every how many seconds do we update "
    "learnt policy weights from the server?",
)
parser.add_argument(
    "--stop-reward",
    type=float,
    default=9999,
    help="Stop once the specified reward is reached.",
)

if __name__ == "__main__":
    args = parser.parse_args()

    client = PolicyClient(
        "http://" + args.server + ":" + str(args.port),
        inference_mode=args.inference_mode,
        update_interval=args.update_interval_local_mode,
    )

    
    env = MultiAgentArena.get_env(instance=True) 
    obs, info = env.reset()
    eid = client.start_episode(training_enabled=not args.no_train)

    # Keep track of the total reward per episode.
    total_rewards_this_episode = 0.0

    # Loop infinitely through the env.
    while True:
        # Get actions from the Policy server given our current obs.
        actions = client.get_action(eid, obs)
        # Apply actions to our env.
        obs, rewards, terminateds, truncateds, infos = env.step(actions)
        total_rewards_this_episode += sum(rewards.values())
        # Log rewards and single-agent terminateds.
        client.log_returns(eid, rewards, infos, multiagent_done_dict=terminateds)
        # Check whether all agents are done and end the episode, if necessary.
        if terminateds["__all__"] or truncateds["__all__"]:
            print("Episode done: Reward={}".format(total_rewards_this_episode))
            if total_rewards_this_episode >= args.stop_reward:
                quit(0)
            # End the episode and reset Unity Env.
            total_rewards_this_episode = 0.0
            client.end_episode(eid, obs)
            obs, info = env.reset()
            # Start a new episode.
            eid = client.start_episode(training_enabled=not args.no_train)