import numpy as np


class Grid:
    def __init__(self, width, height, n_field_types, grid=None):
        self.width = width
        self.height = height
        self.n_field_types = n_field_types
        if grid is None:
            self.multi_dim_grid = np.zeros((n_field_types, width, height))
        else:
            self.multi_dim_grid = grid

    def is_valid_coordinates(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_field_free(self, x, y, dims=()):
        if not dims:
            dims = list(range(self.multi_dim_grid.shape[0]))
        if self.is_valid_coordinates(x, y):
            return self.multi_dim_grid[dims, x, y].sum() == 0

        return False

    def set_value(self, field_ix, x, y, value=1):
        self.multi_dim_grid[field_ix, x, y] = value

    def reset_value(self, field_ix, x, y):
        self.multi_dim_grid[field_ix, x, y] = 0

    def get_value(self, field_ix, x, y):
        return self.multi_dim_grid[field_ix, x, y]

    def get_free_coordinates(self):
        return np.array(np.where(self.get_2d_grid() == 0))

    def get_random_free_coordinates(self):
        indices = self.get_free_coordinates()

        if indices.shape[0] == 0 or indices.shape[1] == 0:
            return None

        return indices[:, np.random.randint(indices.shape[1])]

    def get_free_neighbours(self, x, y):
        free_neighbours = []
        for a, b in ((1, 0), (0, -1), (-1, 0), (0, 1)):
            new_x = x + a
            new_y = y + b

            if self.is_valid_coordinates(new_x, new_y) and self.is_field_free(new_x, new_y):
                free_neighbours.append((new_x, new_y))

        return free_neighbours

    def get_2d_grid(self):
        return self.multi_dim_grid.sum(0)

    def get_grid_for_field_type(self, field_ix):
        return self.multi_dim_grid[field_ix]

    def set_grid_for_field_type(self, field_ix, grid):
        self.multi_dim_grid[field_ix] = grid

    def copy(self):
        new_grid = Grid(
            self.width,
            self.height,
            self.n_field_types
        )

        new_grid.multi_dim_grid = self.multi_dim_grid.copy()

        return new_grid

    def get_occupied_positions(self, field_ix):
        return np.array(np.where(self.multi_dim_grid[field_ix] != 0))


def can_reach_goal(grid, start_pos, end_pos):
    width, height = grid.shape
    start_pos = np.array(start_pos)
    end_pos = np.array(end_pos)

    way_map = np.zeros_like(grid)
    way_map[start_pos[0], start_pos[1]] = 1
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    current_pos = start_pos
    current_path = [start_pos]

    while True:
        dead_end = True
        for direction in directions:
            new_x, new_y = new_pos = (current_pos + direction)
            if (new_pos == end_pos).all():
                return True

            if 0 <= new_x < width and 0 <= new_y < height and (grid + way_map)[new_x, new_y] == 0:
                way_map[new_x, new_y] = 1
                current_path.append(current_pos)
                current_pos = new_pos
                dead_end = False
                break

        if dead_end:
            if len(current_path) > 0:
                current_pos = current_path[-1]
                current_path = current_path[:-1]
            else:
                return False


if __name__ == '__main__':
    a = np.array([[0, 0, 1, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 0],
                  [1, 0, 1, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 0]])
    a = np.rot90(a)

    print(can_reach_goal(a, np.array([0, 5]), np.array([2, 5])))
