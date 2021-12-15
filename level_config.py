import pygame

import ducks
from buttons import fetch_file
from drip import get_obstacles

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((10, 10))  # needed for convert to work


def create_level(number, x_destr, y_destr, x_ind, y_ind, duck_info,
                 change_size=False, x_picture=None, y_picture=None):
    num = str(number)
    if change_size:
        def destr():
            return get_obstacles(fetch_file('pictures', 'destr.png', 'levels', 'level' + num,
                                            x_size=x_picture, y_size=y_picture), x_destr, y_destr)

        def indestr():
            return get_obstacles(fetch_file('pictures', 'indestr.png', 'levels', 'level' + num,
                                            x_size=x_picture, y_size=y_picture), x_ind, y_ind)
    else:
        def destr():
            return get_obstacles(fetch_file('pictures', 'destr.png', 'levels', 'level' + num), x_destr, y_destr)

        def indestr():
            return get_obstacles(fetch_file('pictures', 'indestr.png', 'levels', 'level' + num), x_ind, y_ind)

    def duck_function():
        duck_list = []
        for d in duck_info:
            if len(d) == 2:
                duck_x, duck_y = d
                duck_list.append(ducks.Duck(None, 30, duck_x, duck_y, using_mask=True))
            if len(d) == 3:
                duck_x, duck_y, f = d
                duck_list.append(ducks.Duck(None, 30, duck_x, duck_y, using_mask=True, faculty=f))
        return duck_list

    level = dict({'destr': destr, 'indestr': indestr, 'ducks': duck_function})

    return level


level1 = create_level(1, 340, 240, 340, 440, [(400, 200)])


# level2 config

def level2_destr():
    return (
        get_obstacles(
            fetch_file('pictures', 'destr.png', 'levels', 'level2', x_size=800, y_size=800), 400, 400))


def level2_indestr():
    return (
        get_obstacles(
            fetch_file('pictures', 'indestr.png', 'levels', 'level2'), 340, 440))


def level2_ducks():
    return ([ducks.Duck(None, 30, 100, 350, using_mask=True),
             ducks.Duck(None, 30, 600, 350, using_mask=True, faculty='fupm'),
             ducks.Duck(None, 30, 610, 580, using_mask=True, faculty='fpfe')])


level2 = dict({'destr': level2_destr, 'indestr': level2_indestr,
               'ducks': level2_ducks})


# level3 config

def level3_destr():
    return (
        get_obstacles(
            fetch_file('pictures', 'destr.png', 'levels', 'level3', x_size=800, y_size=800), 400, 400))


def level3_indestr():
    return (
        get_obstacles(
            fetch_file('pictures', 'indestr.png', 'levels', 'level3', x_size=800, y_size=800), 400, 400))


def level3_ducks():
    return ([ducks.Duck(None, 30, 350, 350, using_mask=True),
             ducks.Duck(None, 40, 220, 520, using_mask=True, faculty='dgap'),
             ducks.Duck(None, 30, 450, 570, using_mask=True, faculty='falt')])


level3 = dict({'destr': level3_destr, 'indestr': level3_indestr,
               'ducks': level3_ducks})

levels = [level1, level2, level3]
