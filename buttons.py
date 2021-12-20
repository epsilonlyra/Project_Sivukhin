import os

import pygame


def fetch_file(directory, filename, *directories, file_type=None,
               x_size=None, y_size=None):
    """
    Function for working with files in game folder
    parameters:
    directory : string  first folder in which file is located
    filename : string name of file, including extension
    *directory : string  non-obligatory arguments \
            separated by commas folders on the way from directory to file
    file_type : string file type, by default it us picture, can be changed to\
        'music' or 'other'
    x_size, y_size : int if file is a picture these are its new width and height
    return:
        if file_type is None : pygame.Surface
        if file_type is music : makes pygame.music.load 
        else gets abspath
    """

    path = os.path.abspath(directory)
    for directory in directories:
        path = os.path.join(path, directory)

    if file_type is None:
        if x_size or y_size:
            surf = pygame.image.load((os.path.join(path, filename)))
            surf = pygame.transform.scale(surf, (x_size, y_size))
            return surf
        else:
            return pygame.image.load((os.path.join(path, filename)))
    if file_type == 'music':
        return pygame.mixer.music.load((os.path.join(path, filename)))
    if file_type == 'other':
        return os.path.join(path, filename)


WIDTH = 700
HEIGHT = 800


# screen parametrs

class Picture:

    def __init__(self, x, y, image, *size, angle=None):
        """
        Class for picture drawing
        image : pygame.Surface
        x, y coordinates of center of rectangle
        *size : length, width of pic . If not two arguments are given uses \
            pictures parametrs
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

        self.rot_image_rect = None
        self.rot_image = None

    def draw(self, screen):
        """
        Drawing Picture on given screen
        Parameters:
        screen :  pygame.Surface
        """

        self.rot_image = pygame.transform.rotate(self.image, self.angle)
        self.rot_image_rect = self.rot_image.get_rect(center=self.image_rect.center)
        screen.blit(self.rot_image, self.rot_image_rect)


class Button(Picture):

    def __init__(self, x, y, image, func=None, *size, argument=None):
        """
        Initialize Subclass of Picture
        image : pygame.Surface
        x, y coordinates of center of rectangle
        *size : length, width of pic . If not two arguments are given uses \
            pictures parametrs
        func : function of button
        argument : argument of that function
        """

        self.func = func
        super().__init__(x, y, image, *size)
        self.argument = argument

    def check_click(self, event):
        """
        Checking if user clicked on button
        event : pygame.event.MOUSEBUTTONDOWN
        screen : pygame.Surface
        """
        x = event.pos[0]
        y = event.pos[1]
        if self.image_rect.collidepoint(x, y):
            if self.argument is not None:
                self.func(self.argument)
            else:
                self.func()


icon = fetch_file('pictures', 'icon.jpg')  # icon for app
dgap_cat = fetch_file('pictures', 'cat_dgap.jpg')
Cat = Picture(100, 100, dgap_cat, 100, 100, angle=0)

pygame.font.init()

font = pygame.font.SysFont(None, 30)

# creating surfaces for buttons
button_play_surf = font.render('Play', True, 'red', 'green')
button_pause_surf = font.render('Pause', True, 'green')
button_quit_surf = font.render('Quit', True, 'red')
button_replay_surf = font.render('Retry', True, 'green')
button_sound_surf = font.render('Sound', True, 'green')
level_button_surf = []
for i in range(1, 6):
    level_button_surf.append(font.render('Level' + str(i), False, 'green',
                                         'black'))

# creating Background
BACKGROUND = (fetch_file('pictures', 'lab_corp.png'))
BACKGROUND = pygame.transform.scale(
    BACKGROUND, (WIDTH, HEIGHT))

brick_wall = fetch_file('pictures', 'wall.png')
# creating level end sign
game_over_surf = font.render('Level Finished', True, 'green')

# creating instruction
INSTRUCTIONTEXT = fetch_file('pictures', 'instruction.png')
INSTRUCTION = pygame.Surface((WIDTH, HEIGHT))
INSTRUCTION.blit(BACKGROUND, (0, 0))
INSTRUCTION.blit(INSTRUCTIONTEXT, (
    (WIDTH/2 - round(INSTRUCTIONTEXT.get_width()/2)),
    (HEIGHT/2 - round(INSTRUCTIONTEXT.get_height()/2))))
