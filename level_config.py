import ducks
import pygame
from ducks import *
from buttons import fetch_file
from drip import get_obstacles

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((10, 10)) # это нужно чтобы работал convert

# level1 config

def level1_destr():
    return(
        get_obstacles(
            fetch_file('pictures', 'destr.png','levels', 'level1'), 340, 240))

def level1_indestr():
    return(
        get_obstacles(
        fetch_file('pictures', 'indestr.png','levels', 'level1'), 340, 440))

def level1_ducks():
    return([Duck(ducks.circle_function(200, 200, 10), 30, 400, 200,
                           using_mask = True, faculty = 'fpfe')])


level1 = dict({'destr' : level1_destr, 'indestr' : level1_indestr,
              'ducks' : level1_ducks})

# level2 config

def level2_destr():
    return(
        get_obstacles(
            fetch_file('pictures', 'destr.png','levels', 'level2', x_size = 800, y_size = 800), 400, 400))

def level2_indestr():
    return(
        get_obstacles(
        fetch_file('pictures', 'indestr.png','levels', 'level2'), 340, 440))

def level2_ducks():
    return([Duck(None, 30, 100, 350, using_mask = True),
            Duck(None, 30, 600, 350, using_mask = True, faculty = 'fupm'),
            Duck(None, 30, 610, 580, using_mask = True, faculty = 'fpfe')])

level2 = dict({'destr' : level2_destr, 'indestr' : level2_indestr,
              'ducks' : level2_ducks})

# level3 config

def level3_destr():
    return(
        get_obstacles(
            fetch_file('pictures', 'destr.png','levels', 'level3', x_size = 800, y_size = 800), 400, 400))

def level3_indestr():
    return(
        get_obstacles(
        fetch_file('pictures', 'indestr.png','levels', 'level3', x_size = 800, y_size = 800), 400, 400))

def level3_ducks():
    return([Duck(None, 30, 350, 350, using_mask = True),
            Duck(None, 40, 230, 390, using_mask = True, faculty = 'dgap'),
            Duck(None, 30, 450, 650, using_mask = True, faculty = 'falt')])

level3 = dict({'destr' : level3_destr, 'indestr' : level3_indestr,
              'ducks' : level3_ducks})


levels = [level1, level2, level3]
