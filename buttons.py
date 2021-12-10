import pygame
import os

def fetch_file(directory, filename, *directories, type = None):
    path = os.path.abspath(directory)
    for directory in directories:
        path = os.path.join(path, directory)

    if type ==  None:
        return pygame.image.load((os.path.join(path, filename)))
    if type == 'music':
        return pygame.mixer.music.load((os.path.join(path, filename)))
    if type == 'other':
        return (os.path.join(path, filename))

WIDTH = 700
HEIGHT = 800

class Picture():
    """
    Класс для рисования поверхностей на экране
    """
    
    def __init__(self, x, y, image, *size, angle = None):
        """
        Инициализация класса Picture
        image : pygame.surface object который будет рисоватся
        x, y координаты центра image на screen (оси - стандарт pygame)
        *size : длина, высота . Если будет передано  не два аргумента,
        то будут использованы длина и высота image
        """
        self.x = x
        self.y = y
        if len(size) == 2:
            width = size[0]
            height = size[1]
            self.image = pygame.transform.scale(
            image, (width, height))
            self.image.set_colorkey('white')
        else:
            self.image = image
        if angle:
            self.angle = angle
        else:
            self.angle = 0
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        """
        Рисование Picture на данном экране
        Parameters:
        screen :  pygame.surf.object на котором мы будем рисовать
        """
        #self.image.set_colorkey('black') #почему то неадекватная работа
    
        self.rot_image = pygame.transform.rotate(self.image, self.angle)
        self.rot_image_rect = self.rot_image.get_rect(center =
                                          self.image_rect.center)
        screen.blit(self.rot_image, self.rot_image_rect)
        
        


class Button(Picture):
    
    def __init__(self, x, y, image, func, *size, argument =  None):
        """
        Инициализация класса Picture
        image : pygame.surface object который будет рисоватся
        x, y координаты центра image на screen (оси - стандарт pygame)
        *size : длина, высота изображения.Если будет передано не два аргумента,
        то будут использованы длина и высота image
        func : функция вызываемая при нажатии кнопки
        """
        
        self.func = func
        super().__init__(x, y, image, *size)
        self.argument = argument

    def check_click(self, event):
        x = event.pos[0]
        y = event.pos[1]
        if self.image_rect.collidepoint(x, y):
            if self.argument:
                self.func(self.argument)
            else:
                self.func()
    

icon = fetch_file('pictures', 'icon.jpg') # icon for app
dgap_cat = fetch_file('pictures', 'cat_dgap.jpg')
TEST = fetch_file('pictures', 'TEST.png', 'TEST')
Cat = Picture(200, 700, dgap_cat, 100, 100, angle = 0)

template_surf = pygame.Surface((100, 100))
changable_surf = template_surf

pygame.font.init()

font = pygame.font.SysFont(None, 30)

button_play_surf = font.render('Play', True, 'red', 'yellow')
button_pause_surf = font.render('Pause', True, 'red', 'black')
button_quit_surf = font.render('Quit', True, 'red', 'black')
button_replay_surf = font.render('Retry', True, 'red', 'black')
level_button_surf = []
for i in range(1, 4):
    level_button_surf.append(font.render('Level' + str(i), True, 'red',
                                         'black'))
BACKGROUND = (fetch_file('pictures', 'lab_corp.png'))
BACKGROUND = pygame.transform.scale(
            BACKGROUND, (WIDTH, HEIGHT))




        

