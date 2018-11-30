import numpy as np
import gridworld_displayer

config1 = [
    # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
    [0, 3, 0, 3, 0, 3, 0, 0, 0, 0],  # 2
    [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],  # 3
    [3, 0, 3, 0, 0, 3, 0, 0, 3, 3],  # 4
    [3, 0, 3, 3, 3, 3, 0, 0, 3, 2],  # 5
    [0, 0, 3, 0, 0, 0, 0, 0, 3, 0],  # 6
    [0, 3, 0, 0, 3, 3, 3, 0, 3, 0],  # 7
    [3, 0, 0, 0, 3, 0, 3, 3, 3, 0],  # 8
    [0, 0, 0, 3, 3, 0, 0, 0, 3, 0],  # 9
    [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
]


def to_state(grid_2d):
    x = np.tile(grid_2d, [4, 1, 1])
    x = (x == np.array([1, 2, 4, 3]).reshape([4, 1, 1])).astype(int)
    x = np.transpose(x, [0, 2, 1])
    return x


if __name__ == '__main__':
    s = to_state(config1)
    print(s)
    d = gridworld_displayer.PyGameDisplayer(10, 10)
    d.display(s)
