import pygame
from pygame.draw import *

class Picture():
    """
    Класс для рисования поверхностей на экране
    """
    
    def __init__(self, x, y, image, width, height, screen):
        """
        Инициализация
        Parameters:
        screen :  pygame.surf.object на котороv мы будем рисовать
        image : pygame.surface object который будет рисоватся
        x, y координаты центра image на screen (оси - стандарт pygame

        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(
            image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, (self.x - self.width / 2, self.y - 
                                self.height / 2))


class Button(Picture):
    def __init__( self, x, y, image, width, height, screen):
        super.init( x, y, image, width, height, screen)
    
    
        

