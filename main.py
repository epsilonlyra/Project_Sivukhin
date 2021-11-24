import pygame
from pygame.draw import *
from buttons import *
import os



WIDTH = 700
HEIGHT = 800
FPS = 30

def fetch_file(directory, filename):
    return(os.path.join(os.path.abspath(directory), filename))
        
pygame.init()

icon = pygame.image.load(fetch_file('pictures', 'icon.jpg'))
pygame.display.set_icon(icon)
pygame.display.set_caption(('Проект Сивухин'))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


finished = False
while not finished:
    screen.fill('white')
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        
pygame.quit()
