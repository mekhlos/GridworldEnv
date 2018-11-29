import gridworld
import gridworld_displayer


class GridworldEnv:
    def __init__(self, width, height):
        displayer = gridworld_displayer.PyGameDisplayer(width, height)
        self.gridworld = gridworld.GridWorld(width, height, displayer)

    def get_reward(self):
        if self.gridworld.is_done():
            return 10

        return -1

    def take_action(self, action):
        self.gridworld.take_action(action)
        self.gridworld.display()
        return self.gridworld.get_state(), \
               self.get_reward(), \
               self.gridworld.is_done(), \
               []

    def reset(self):
        self.gridworld.reset()

    @staticmethod
    def get_action_space():
        return gridworld.Actions.get_actions()
