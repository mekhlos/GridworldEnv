import numpy as np


def is_valid_coordinate(coords, width, height):
    return 0 <= coords[0] < width and 0 <= coords[1] < height


class Grid:
    def __init__(self, width, height, n_field_types):
        self.height = height
        self.width = width
        self.n_field_types = n_field_types
        self.multi_dim_grid = np.zeros((n_field_types, width, height))

    def is_valid_coordinates(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_field_free(self, x, y):
        if self.is_valid_coordinates(x, y):
            return self.multi_dim_grid[:, x, y].sum() == 0

        return False

    def set_value(self, field_ix, x, y, value):
        self.multi_dim_grid[field_ix, x, y] = value

    def get_value(self, field_ix, x, y):
        return self.multi_dim_grid[field_ix, x, y]

    def get_free_coordinates(self):
        return np.array(np.where(self.multi_dim_grid.sum(0) == 0))

    def get_random_free_coordinates(self):
        indices = self.get_free_coordinates()

        if indices.shape[0] == 0:
            return []

        return indices[:, np.random.randint(indices.shape[1])]

    def get_free_neighbours(self, x, y):
        free_neighbours = []
        for a, b in ((1, 0), (0, -1), (-1, 0), (0, 1)):
            new_x = x + a
            new_y = y + b

            if self.is_valid_coordinates(new_x, new_y) and self.is_field_free(new_x, new_y):
                free_neighbours.append((new_x, new_y))

        return free_neighbours


def can_reach_goal(grid, start_pos, end_pos):
    width, height = grid.shape

    way_map = np.zeros_like(grid)
    way_map[start_pos[0], start_pos[1]] = 1
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    current_pos = start_pos
    current_path = [start_pos]

    while True:
        dead_end = True
        for direction in directions:
            new_x, new_y = new_pos = (current_pos + direction)

            if 0 <= new_x < width and 0 <= new_y < height and (grid + way_map)[new_x, new_y] == 0:
                if (new_pos == end_pos).all():
                    return True

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
