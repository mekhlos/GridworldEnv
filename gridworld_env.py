import gridworld
import gridworld_displayer


class GridworldEnv:
    def __init__(self, width, height, **kwargs):
        self._displayer = gridworld_displayer.PyGameDisplayer(width, height)
        self._gridworld = gridworld.GridWorld(width, height, **kwargs)
        self.prev_state = None
        self.state = None

    def get_reward(self):
        if self._gridworld.is_done():
            return 10

        if self.prev_state is not None and self.state is not None and (self.prev_state[0] == self.state[0]).all():
            return -2

        return -1

    def take_action(self, action):
        self._gridworld.take_action(action)

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

    def display(self):
        self._displayer.display(self._gridworld.get_state())

    @staticmethod
    def get_action_space():
        return gridworld.Actions.get_actions()


if __name__ == '__main__':
    import numpy as np
    import time

    env = GridworldEnv(4, 4)
    actions = env.get_action_space()
    for i in range(10):
        env.take_action(np.random.choice(actions))
        print(env.get_reward())
        env.display()
        time.sleep(0.2)
