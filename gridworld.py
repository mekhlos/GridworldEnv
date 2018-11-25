import numpy as np
import gridworld_displayer
import helpers
import random

DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def is_valid_coordinate(coords, width, height):
    return 0 <= coords[0] < width and 0 <= coords[1] < height


def can_reach_goal(grid, start_pos, end_pos):
    way_map = np.zeros_like(grid)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    current_pos = start_pos
    current_path = []
    while True:
        for direction in directions:
            new_pos = (current_pos + direction)
            if is_valid_coordinate(new_pos, *grid.shape[::-1]) and (grid + way_map)[new_pos[::-1]] == 0:
                if (new_pos == end_pos).all():
                    return True

                way_map[new_pos[::-1]] = 1
                current_path.append(new_pos)
                current_pos = new_pos
                break

            if len(current_path) > 0:
                current_pos = current_path[-1]
                current_path = current_path[:-1]
            else:
                return False


class WallGenerator:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def generate_wall(self, max_length):
        pass


class GridWorld:
    PLAYER_DIM = 0
    GOAL_DIM = 1
    PIT_DIM = 2
    WALL_DIM = 3

    def __init__(self, width, height, displayer, random_seed=None):
        self.height = height
        self.width = width
        self.grid = None
        self.displayer = displayer
        self.player_position = None
        self.goal_position = None

        if random_seed:
            np.random.seed(random_seed)

        self._initialise_grid()

    def _place_player(self):
        x, y = self.grid.get_random_free_coordinates()
        self.grid.set_value(self.PLAYER_DIM, x, y, 1)
        self.player_position = (x, y)

    def _place_goal(self):
        x, y = self.grid.get_random_free_coordinates()
        self.grid.set_value(self.GOAL_DIM, x, y, 1)
        self.goal_position = (x, y)

    def _place_walls(self, density):
        start_position = self.grid.get_random_free_coordinates()
        avg_wall_length = (width + height) // 2
        max_wall_length = avg_wall_length * 2
        n_bricks = np.clip(np.random.normal(avg_wall_length, avg_wall_length * 0.7), 1, max_wall_length)
        self._place_walls_recursive(start_position, int(n_bricks), random.sample(DIRECTIONS, 1)[0])

    def _place_walls_recursive(self, start_pos, bricks_left, direction):
        x, y = start_pos
        if bricks_left > 0 and self.grid.is_field_free(x, y):
            self.grid.set_value(self.WALL_DIM, x, y, 1)
            if helpers.can_reach_goal(self.grid.get_2d_grid(), self.player_position, self.goal_position):
                new_direction = random.sample(DIRECTIONS, 1)[0]
                self._place_walls_recursive(start_pos + direction, bricks_left - 1, new_direction)
            else:
                self.grid.set_value(self.WALL_DIM, x, y, 0)

    def _initialise_grid(self):
        self.grid = helpers.Grid(width, height, 4)
        self._place_player()
        self._place_goal()
        for i in range(10):
            self._place_walls(0.1)

    def display(self):
        self.displayer.display(self.grid.multi_dim_grid)

    def reset(self):
        self._initialise_grid()

    def take_action(self):
        pass


if __name__ == '__main__':
    width, height = 10, 10
    # displayer = gridworld_displayer.ConsoleDisplayer(width, height)
    displayer = gridworld_displayer.PyGameDisplayer(width, height)
    gridworld = GridWorld(width, height, displayer)
    gridworld.display()
