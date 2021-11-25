import pygame
import os

def fetch_file(directory, filename):
    return(os.path.join(os.path.abspath(directory), filename))


class Picture():
    """
    Класс для рисования поверхностей на экране
    """
    
    def __init__(self, x, y, image, width, height):
        """
        Инициализация класса Button
        image : pygame.surface object который будет рисоватся
        x, y координаты центра image на screen (оси - стандарт pygame)
        width, height - длина и ширина 

        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(
            image, (width, height))

    def draw(self, screen):
        """
        Рисование Picture на данном экране
        Parameters:
        screen :  pygame.surf.object на котором мы будем рисовать
        """
        #self.image.set_colorkey('white') почему то неадекватная работа
        screen.blit(self.image, (self.x - self.width / 2, self.y - 
                                self.height / 2))


class Button(Picture):
    
    def __init__( self, x, y, image, func, *args):
        
        self.func = func
        if len(args) == 2:
            width = args[0]
            height = args[1]
        else:
            width = image.get_width()
            height = image.get_height()
        super().__init__(x, y, image, width, height)

    def check_click(self, event):
        x_click = event.pos[0]
        y_click = event.pos[1]
        if (x_click - self.x <= self.width / 2) and (x_click - self.x >= - self.width / 2):
            if (y_click - self.y <= self.height / 2) and (y_click - self.y >= - self.height / 2):
                self.func()
    

icon = pygame.image.load(fetch_file('pictures', 'icon.jpg')) # icon for app

def printsus():
    print('sus')

template_surf = pygame.Surface((100, 100))
changable_surf = template_surf

pygame.font.init()

font = pygame.font.SysFont(None, 30)
img = font.render('Click me!', True, 'red', 'black')

button1 = Button(100, 100, img, printsus)





        

