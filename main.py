import gridworld_env
import time
import numpy as np


def run_actions(env: gridworld_env.GridworldEnv, actions):
    env.reset()
    for action in actions:
        env.take_action(action)
        time.sleep(1)


if __name__ == '__main__':
    env = gridworld_env.GridworldEnv(10, 10)
    all_actions = env.get_action_space()
    actions = np.random.choice(all_actions, 10)
    run_actions(env, actions)
