import numpy as np
import pygame
import settings


class Displayer:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class ConsoleDisplayer(Displayer):

    def __init__(self, width, height):
        super().__init__(width, height)

    def display(self, multi_dim_grid):
        field_symbols = {settings.PLAYER_DIM: ' o ',
                         settings.GOAL_DIM: ' $ ',
                         settings.PIT_DIM: ' X ',
                         settings.WALL_DIM: '‡‡‡'}

        res = '-' * (self.width * 3 + 2) + '\n'
        for i in range(self.height):
            res += '|'
            for j in range(self.width):
                field = multi_dim_grid[:, i, j]
                if field.sum() > 1:
                    raise Exception('There should be only one symbol on every field...')
                elif field.sum() == 1:
                    field_type = np.where(field > 0)[0][0]
                    res += f'{field_symbols[field_type]}'
                else:
                    res += '   '

            res += '|\n'

        res += '-' * (self.width * 3 + 2)
        print(res)


class PyGameDisplayer(Displayer):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (120, 200, 100)
    YELLOW = (255, 200, 100)

    BACKGROUND_COLOUR = (255, 255, 255)
    OBSTACLE_COLOUR = (10, 10, 10)
    PIT_COLOUR = (100, 50, 0)
    ROBOT_COLOUR = (10, 100, 10)

    FIELD_BASE_WIDTH = 70
    FIELD_WIDTH = 69
    FIELD_PADDING = (FIELD_BASE_WIDTH - FIELD_WIDTH) // 2

    def __init__(self, width, height):
        super().__init__(width, height)
        pygame.init()
        self.screen = pygame.display.set_mode((width * self.FIELD_BASE_WIDTH, height * self.FIELD_BASE_WIDTH))
        self.screen.fill(self.BACKGROUND_COLOUR)

    def display(self, grid):
        self.screen.fill(self.BACKGROUND_COLOUR)

        for i in range(self.height):
            for j in range(self.width):
                start_x, start_y = i * self.FIELD_BASE_WIDTH, j * self.FIELD_BASE_WIDTH
                mid_x, mid_y = start_x + self.FIELD_BASE_WIDTH // 2, start_y + self.FIELD_BASE_WIDTH // 2
                field_start_x = start_x + self.FIELD_PADDING
                field_start_y = start_y + self.FIELD_PADDING

                self.draw_field(field_start_x, field_start_y)

                if grid[settings.PLAYER_DIM, i, j] == 1:
                    self.draw_robot(mid_x, mid_y)
                if grid[settings.GOAL_DIM, i, j] == 1:
                    self.draw_goal(mid_x, mid_y)
                if grid[settings.WALL_DIM, i, j] == 1:
                    self.draw_wall(mid_x, mid_y)

        pygame.display.update()

    def draw_field(self, x, y):
        pygame.draw.rect(self.screen, self.BLACK, (x, y, self.FIELD_WIDTH, self.FIELD_WIDTH), 1)

    def draw_robot(self, x, y):
        # pygame.draw.circle(self.screen, ROBOT_COLOUR, (x, y), 10, 0)
        self.draw_figure(x, y)

    def draw_goal(self, x, y):
        font = pygame.font.Font(None, 80)
        text = font.render("$", 2, self.GREEN)
        self.screen.blit(text, (x - 15, y - 25, 50, 50))

    def draw_wall(self, x, y):
        r = self.FIELD_WIDTH // 2
        pygame.draw.lines(self.screen, self.OBSTACLE_COLOUR, False, [(x - r, y - 1), (x + r - 1, y - 1)], 20)
        pygame.draw.lines(self.screen, self.OBSTACLE_COLOUR, False, [(x - 1, y - r), (x - 1, y + r - 1)], 20)

    def draw_figure(self, x_mid, y_mid):
        head_y = y_mid - 20
        body_x = x_mid - 6
        body_y = y_mid - 9
        hand_y = y_mid - 3
        l_hand_x = x_mid - 10
        r_hand_x = x_mid + 10
        l_leg_x = x_mid - 5
        r_leg_x = x_mid + 4
        leg_y = y_mid + 20

        pygame.draw.circle(self.screen, self.BLACK, (x_mid, head_y), 8, 1)

        pygame.draw.lines(self.screen, self.OBSTACLE_COLOUR, False,
                          [(l_hand_x - 5, hand_y + 5), (l_hand_x + 5, hand_y - 5)], 3)
        pygame.draw.lines(self.screen, self.OBSTACLE_COLOUR, False,
                          [(r_hand_x - 5, hand_y - 5), (r_hand_x + 5, hand_y + 5)], 3)

        pygame.draw.lines(self.screen, self.OBSTACLE_COLOUR, False,
                          [(l_leg_x + 2, leg_y - 7), (l_leg_x - 2, leg_y + 10)], 3)
        pygame.draw.lines(self.screen, self.OBSTACLE_COLOUR, False,
                          [(r_leg_x - 2, leg_y - 7), (r_leg_x + 2, leg_y + 10)], 3)

        pygame.draw.rect(self.screen, self.YELLOW, (body_x, body_y, 12, 24), 0)


if __name__ == '__main__':
    d = PyGameDisplayer(5, 5)
    a = (np.random.rand(5, 5) * 5).round(0)
    d.display(a)
