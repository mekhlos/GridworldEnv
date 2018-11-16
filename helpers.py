import numpy as np


def is_valid_coordinate(coords, width, height):
    return 0 <= coords[0] < width and 0 <= coords[1] < height


class Grid:
    def __init__(self, multi_dim_grid):
        self.multi_dim_grid = multi_dim_grid
        self.height, self.width = multi_dim_grid.shape

    def is_valid_coordinates(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_value(self):
        pass


def can_reach_goal(grid, start_pos, end_pos):
    def get_value_at(grid2, pos):
        return grid2[pos[1], pos[0]]

    way_map = np.zeros_like(grid)
    way_map[start_pos[1], start_pos[0]] = 1
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    current_pos = start_pos
    current_path = [start_pos]
    while True:
        dead_end = True
        for direction in directions:
            new_pos = (current_pos + direction)

            if is_valid_coordinate(new_pos, *grid.shape[::-1]) and get_value_at(grid + way_map, new_pos) == 0:
                if (new_pos == end_pos).all():
                    return True

                way_map[new_pos[1], new_pos[0]] = 1
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


a = np.array([[0, 0, 1, 0],
              [0, 1, 0, 0],
              [0, 0, 0, 0],
              [1, 0, 1, 0],
              [0, 1, 1, 0],
              [0, 0, 0, 0]])

print(can_reach_goal(a, np.array([0, 5]), np.array([2, 5])))
