import gridworld_env
import time
import numpy as np


def run_actions(env: gridworld_env.GridworldEnv, actions):
    env.reset()
    for action in actions:
        print(action)
        _, _, is_done, _ = env.take_action(action)
        env.display()
        time.sleep(1)
        if is_done:
            break


if __name__ == '__main__':
    env = gridworld_env.GridworldEnv(2, 8)
    all_actions = env.get_action_space()
    actions = np.random.choice(all_actions, 100)
    run_actions(env, actions)
