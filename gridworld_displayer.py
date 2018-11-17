import numpy as np


class Displayer:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class ConsoleDisplayer(Displayer):
    PLAYER_DIM = 0
    GOAL_DIM = 1
    PIT_DIM = 2
    WALL_DIM = 3

    FIELD_SYMBOLS = {PLAYER_DIM: ' o ', GOAL_DIM: ' $ ', PIT_DIM: ' X ', WALL_DIM: '---'}

    def __init__(self, width, height):
        super().__init__(width, height)

    def display(self, multi_dim_grid):
        res = '-' * (self.width * 3 + 2) + '\n'
        for i in range(self.height):
            res += '|'
            for j in range(self.width):
                field = multi_dim_grid[:, i, j]
                if field.sum() > 1:
                    raise Exception('There should be only one symbol on every field...')
                elif field.sum() == 1:
                    field_type = np.where(field > 0)[0][0]
                    res += f'{self.FIELD_SYMBOLS[field_type]}'
                else:
                    res += '   '

            res += '|\n'

        res += '-' * (self.width * 3 + 2)
        print(res)


class PyGameDisplayer(Displayer):
    def __init__(self, width, height):
        super().__init__(width, height)
