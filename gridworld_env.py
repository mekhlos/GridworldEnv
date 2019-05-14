import gridworld
import gridworld_displayer
import settings
import numpy as np


class GridworldEnv:
    def __init__(self, width, height, **kwargs):
        self._displayer = gridworld_displayer.PyGameDisplayer(width, height)
        self._gridworld = gridworld.GridWorld(width, height, **kwargs)
        self.prev_state = None
        self.state = self._gridworld.get_state()

    def get_reward(self):
        if self._gridworld.is_done():
            return 1

        if np.logical_and(self.state[settings.PIT_DIM], self.state[settings.PLAYER_DIM]).any():
            return -10

        return -0.001

    def update(self, action):
        self._gridworld.update(gridworld.Actions.get_actions()[action])

        self.prev_state = self.state if self.state is not None else None
        self.state = self._gridworld.get_state()

        return self.state, \
               self.get_reward(), \
               self._gridworld.is_done(), \
               []

    def reset(self):
        self._gridworld.reset()
        self.prev_state = None
        self.state = self._gridworld.get_state()
        return self.state

    def get_state(self):
        return self.state

    def display(self):
        self._displayer.display(self._gridworld.get_state())

    @staticmethod
    def get_action_space():
        return list(range(len(gridworld.Actions.get_actions())))

    def close(self):
        pass


if __name__ == '__main__':
    import numpy as np
    import time

    env = GridworldEnv(4, 4)
    actions = env.get_action_space()
    for i in range(10):
        env.update(np.random.choice(actions))
        print(env.get_reward())
        env.display()
        time.sleep(0.2)
