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
                           using_mask = True)])


level1 = dict({'destr' : level1_destr, 'indestr' : level1_indestr,
              'ducks' : level1_ducks})

def level2_destr():
    return(
        get_obstacles(
            fetch_file('pictures', 'destr.png','levels', 'level2'), 340, 240))

def level2_indestr():
    return(
        get_obstacles(
        fetch_file('pictures', 'indestr.png','levels', 'level2'), 340, 440))

def level2_ducks():
    return([Duck(ducks.circle_function(200, 200, 10), 30, 200, 200,
                           using_mask = True)])

level2 = dict({'destr' : level2_destr, 'indestr' : level2_indestr,
              'ducks' : level2_ducks})

levels = [level1, level2]
