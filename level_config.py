import json
import os

import numpy
import pygame

import ducks
import mech
from buttons import fetch_file
from drip import get_obstacles

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((10, 10))  # needed for convert to work


def create_level(number, x_destr, y_destr, x_ind, y_ind, duck_info, mech_info,
                 x_picture=None, y_picture=None, water_generated=False):
    """
    Function  to make levels
    returns  a dictionary which holds functions which return level stats
    parameters:
    number : int(1-5) level number is used to determine which folder to use \
    to get surfaces for level
    x_destr, y_destr : int coordinates of left corner of destructible surface
    x_ind, y_ind :  int coordinates of left corner of indestructible surface
    duck_info : a list holding lists of 2 or 3 elements which describe \
    ducks coordinates(int) and department (string)
    Non-obligatory params:
    x_picture, y_picture : positive int new size of picture
    """

    num = str(number)
    # following functions return a pygame.Surface objects

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
        """
        Returns a list of Duck class examples\
        from duck.info array
        """
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

    def mech_function():
        """
        Returns a list of Mech examples from mech.info array
        """
        mech_list = []
        for mechanism in mech_info:
            col_x, col_y, col_angle, body_x, body_y, body_angle, move_angle, color = mechanism
            mech_list.append(mech.Mech(col_x, col_y, col_angle, body_x, body_y, body_angle, move_angle, color))

        return mech_list

    level = dict({'destr': destr, 'indestr': indestr, 'ducks': duck_function, 'mechs': mech_function,
                  'water_generated': water_generated})

    return level


def load_water(number):
    """
    Return r_vector numpy array with water coordinates
    """
    num = str(number)
    with open(os.path.join('pictures', 'levels', 'level' + num, 'water_position.json')) as file:
        data = json.load(file)
    with open(os.path.join('pictures', 'levels', 'level' + num, 'water_position.json'), 'w') as file:
        json.dump(data, file)
    data = numpy.array(data)
    return data


def record_water(number, array: numpy.ndarray):
    """
    Writes (numpy) array in water_position.json in level_number file
    (This function is used only when creating new levels)
    """
    arr = array.tolist()
    num = str(number)
    with open(os.path.join('pictures', 'levels', 'level' + num, 'water_position.json')) as file:
        data = json.load(file)
    with open(os.path.join('pictures', 'levels', 'level' + num, 'water_position.json'), 'w') as file:
        json.dump(arr, file)
    return data


level1 = create_level(1, 340, 240, 340, 440, [(400, 200)], [(0, 0, 0, 100, 50, 0, 0, 'orange')])

level2 = create_level(2, 400, 400, 340, 440,
                      [(600, 350, 'fupm'), (610, 580, 'fpfe'), (100, 350)], [],
                      x_picture=800, y_picture=800, water_generated=True
                      )

level3 = create_level(3, 400, 440, 400, 440, [(350, 350), (220, 520, 'dgap'), (450, 570, 'falt')], [],
                      x_picture=800, y_picture=800)

level4 = create_level(4, 350, 440, 350, 440, [(625, 670), (360, 730, 'dgap'), (268, 350, 'falt')],
                      [(0, 450, 0, 580, 240, 0, 0, 'orange')])

level5 = create_level(5, 350, 440, 350, 440, [(327, 700), (327, 270, 'dgap'), (75, 135, 'falt')],
                      [(45, 125, 0, 290, 150, 0, 0, 'orange'), (60, 125, 0, 300, 350, 0, 0, 'blue')])

levels = [level1, level2, level3, level4, level5]
