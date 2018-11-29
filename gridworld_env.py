import gridworld
import gridworld_displayer


class GridworldEnv:
    def __init__(self, width, height):
        self._displayer = gridworld_displayer.PyGameDisplayer(width, height)
        self._gridworld = gridworld.GridWorld(width, height)

    def get_reward(self):
        if self._gridworld.is_done():
            return 10

        return -1

    def take_action(self, action):
        self._gridworld.take_action(action)
        return self._gridworld.get_state(), \
               self.get_reward(), \
               self._gridworld.is_done(), \
               []

    def reset(self):
        self._gridworld.reset()

    def display(self):
        self._displayer.display(self._gridworld.get_state())

    @staticmethod
    def get_action_space():
        return gridworld.Actions.get_actions()
