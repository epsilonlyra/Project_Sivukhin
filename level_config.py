import pygame

import ducks
from buttons import fetch_file
from drip import get_obstacles

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((10, 10))  # needed for convert to work


def create_level(number, x_destr, y_destr, x_ind, y_ind, duck_info,
                 x_picture=None, y_picture=None):
    """
    Function makes level (expand)
    """

    num = str(number)

    if (x_picture is None) or (y_picture is None):

        def destr():
            return get_obstacles(
                fetch_file('pictures', 'destr.png', 'levels', 'level' + num),
                x_destr, y_destr)

        def indestr():
            return get_obstacles(
                fetch_file('pictures', 'indestr.png', 'levels', 'level' + num),
                x_ind, y_ind)

    else:

        def destr():
            return get_obstacles(
                fetch_file('pictures', 'destr.png', 'levels', 'level' + num,
                           x_size=x_picture, y_size=y_picture),
                x_destr, y_destr)

        def indestr():
            return get_obstacles(
                fetch_file('pictures', 'indestr.png', 'levels', 'level' + num,
                           x_size=x_picture, y_size=y_picture),
                x_ind, y_ind)

    def duck_function():
        duck_list = []
        for d in duck_info:
            if len(d) == 2:
                duck_x, duck_y = d
                duck_list.append(ducks.Duck(30,
                                            duck_x, duck_y))
            if len(d) == 3:
                duck_x, duck_y, f = d
                duck_list.append(ducks.Duck(30, duck_x,
                                            duck_y, faculty=f))
        return duck_list

    level = dict({'destr': destr, 'indestr': indestr, 'ducks': duck_function})

    return level


level1 = create_level(1, 340, 240, 340, 440, [(400, 200)])

level2 = create_level(2, 400, 400, 340, 440,
                      [(600, 350, 'fupm'), (610, 580, 'fpfe'), (100, 350)],
                      x_picture=800, y_picture=800
                      )

level3 = create_level(3, 400, 440, 400, 440, [(350, 350), (220, 520, 'dgap'),
                                              (450, 570, 'falt')],
                      x_picture=800, y_picture=800)

levels = [level1, level2, level3]
