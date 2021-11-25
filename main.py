import pygame
from pygame.draw import *
from buttons import *



WIDTH = 700
HEIGHT = 800
FPS = 30


pygame.display.set_icon(icon)
pygame.display.set_caption(('Проект Сивухин'))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


finished = False
while not finished:
    screen.fill('white')
    button1.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            button1.check_click(event)
        
pygame.quit()
