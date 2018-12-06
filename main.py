import gridworld_env
import time
import numpy as np
from grid_configs import configs


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
    # env = gridworld_env.GridworldEnv(4, 4)
    env = gridworld_env.GridworldEnv(5, 5, grid=configs.to_state(configs.config2))
    all_actions = env.get_action_space()
    for i in range(10):
        actions = np.random.choice(all_actions, 8)
        run_actions(env, actions)
        env.reset()
        print('reset')
