import numpy as np
import gridworld_displayer
import helpers
import random
import settings

from utils import logging_helper

DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]


class WallGenerator:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def generate_wall(self, max_length):
        pass


class Actions:
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'

    @staticmethod
    def get_direction(action):
        if action == Actions.LEFT:
            return DIRECTIONS[0]
        elif action == Actions.RIGHT:
            return DIRECTIONS[2]
        elif action == Actions.UP:
            return DIRECTIONS[1]
        elif action == Actions.DOWN:
            return DIRECTIONS[3]
        else:
            raise Exception('Unknown action...')

    @staticmethod
    def get_actions():
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN]

    def __getitem__(self, ix):
        return Actions.get_actions()[ix]


class ResetSettings:
    def __init__(self, reset_agent=False, reset_goal=False, reset_walls=False):
        self.reset_agent = reset_agent or reset_walls
        self.reset_goal = reset_goal or reset_walls
        self.reset_walls = reset_walls


class GridWorld:
    def __init__(self, width, height, grid=None, reset_settings=ResetSettings(), random_seed=None):
        self._logger = logging_helper.get_logger(self.__class__.__name__)
        self.height = height
        self.width = width
        self.n_wall_chunks = (width + height) // 2
        self.grid = None
        if grid is None:
            self.saved_grid = None
        else:
            self.saved_grid = helpers.Grid(width, height, settings.N_DIMS, grid)
        self.player_position = None
        self.goal_position = None
        self.reset_settings = reset_settings

        if random_seed:
            np.random.seed(random_seed)

        self._initialise_grid()

    def _place_player(self):
        if self.saved_grid is None or self.reset_settings.reset_agent:
            x, y = self.grid.get_random_free_coordinates()
            self.grid.set_value(settings.PLAYER_DIM, x, y, 1)
            self.player_position = (x, y)
        else:
            self.grid.set_grid_for_field_type(
                settings.PLAYER_DIM,
                self.saved_grid.get_grid_for_field_type(settings.PLAYER_DIM)
            )

            self.player_position = tuple(self.saved_grid.get_occupied_positions(settings.PLAYER_DIM).squeeze())

    def _place_goal(self):
        if self.saved_grid is None or self.reset_settings.reset_goal:
            x, y = self.grid.get_random_free_coordinates()
            self.grid.set_value(settings.GOAL_DIM, x, y, 1)
            self.goal_position = (x, y)
        else:
            self.grid.set_grid_for_field_type(
                settings.GOAL_DIM,
                self.saved_grid.get_grid_for_field_type(settings.GOAL_DIM)
            )

            self.goal_position = tuple(self.saved_grid.get_occupied_positions(settings.GOAL_DIM).squeeze())

    def _place_walls(self):
        if self.saved_grid is None or self.reset_settings.reset_walls:
            start_position = self.grid.get_random_free_coordinates()
            if start_position is not None:
                avg_wall_length = (self.width + self.height) // 2
                max_wall_length = avg_wall_length * 2
                n_bricks = np.clip(np.random.normal(avg_wall_length, avg_wall_length * 0.7), 1, max_wall_length)
                self._place_walls_recursive(start_position, int(n_bricks), random.sample(DIRECTIONS, 1)[0])
        else:
            self.grid.set_grid_for_field_type(
                settings.WALL_DIM,
                self.saved_grid.get_grid_for_field_type(settings.WALL_DIM)
            )

    def _place_walls_recursive(self, start_pos, bricks_left, direction):
        x, y = start_pos
        if bricks_left > 0 and self.grid.is_field_free(x, y):
            self.grid.set_value(settings.WALL_DIM, x, y, 1)
            if helpers.can_reach_goal(self.grid.get_2d_grid(), self.player_position, self.goal_position):
                new_direction = random.sample(DIRECTIONS, 1)[0]
                self._place_walls_recursive(start_pos + direction, bricks_left - 1, new_direction)
            else:
                self.grid.set_value(settings.WALL_DIM, x, y, 0)

    def _initialise_grid(self):
        self.grid = helpers.Grid(self.width, self.height, 4)
        self._place_player()
        self._place_goal()
        for i in range(self.n_wall_chunks):
            self._place_walls()

        self.saved_grid = self.grid.copy()

    def reset(self):
        self._initialise_grid()

    def is_done(self):
        return self.player_position == self.goal_position

    def get_state(self):
        return self.grid.multi_dim_grid.copy()

    def take_action(self, action_name):
        direction = Actions.get_direction(action_name)
        new_position = np.array(self.player_position) + direction

        if self.grid.is_field_free(*new_position) or all(new_position == self.goal_position):
            self.grid.set_value(settings.PLAYER_DIM, *new_position)
            self.grid.reset_value(settings.PLAYER_DIM, *self.player_position)
            self.player_position = tuple(new_position)
        else:
            # self._logger.debug('Invalid new position...')
            pass


if __name__ == '__main__':
    import time

    rs = ResetSettings(True, False, False)
    width, height = 10, 10
    displayer = gridworld_displayer.PyGameDisplayer(width, height)
    gridworld = GridWorld(width, height, rs)
    displayer.display(gridworld.get_state())
    time.sleep(1)

    gridworld.take_action(Actions.UP)
    displayer.display(gridworld.get_state())
    time.sleep(1)

    gridworld.take_action(Actions.UP)
    displayer.display(gridworld.get_state())
    time.sleep(1)

    gridworld.take_action(Actions.LEFT)
    displayer.display(gridworld.get_state())
    time.sleep(1)

    gridworld.take_action(Actions.RIGHT)
    displayer.display(gridworld.get_state())
    time.sleep(1)

    gridworld.take_action(Actions.DOWN)
    displayer.display(gridworld.get_state())
    time.sleep(1)
