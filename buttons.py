import os

import pygame


def fetch_file(directory, filename, *directories, file_type=None,
               x_size=None, y_size=None):
    """
    Функция для работы с файлами
    parametres:
    directory : string  первая папка в  которой находится файл
    filename : string имя файла, включая расширения
    *directory : string  необязательный аргументы,
            перечисленные через запятую папки на пути к файлу от directory
    file_type : string тип файла по дефолту считается что файл картинка,
                music - музыкальной, other иной
    x_size, y_sizе : int если тип файла картинка(None) то эти параметры его
        нового размера
    return:
        если file_type is None : pygame.Surface
        eсли file_type is music : сделает pygame.music.load файла
        иначе вернет abspath
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
        Класс для рисования картинкок
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

        self.rot_image_rect = None
        self.rot_image = None

    def draw(self, screen):
        """
        Рисование Picture на данном экране
        Parameters:
        screen :  pygame.surf.object на котором мы будем рисовать
        """

        self.rot_image = pygame.transform.rotate(self.image, self.angle)
        self.rot_image_rect = self.rot_image.get_rect(center=self.image_rect.center)
        screen.blit(self.rot_image, self.rot_image_rect)


class Button(Picture):

    def __init__(self, x, y, image, func=None, *size, argument=None):
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
        """
        Проверка на клик пользователя по кнопке и выполнение функционала кнопки
        Кроме того рисование кнопки на данном экране
        event : pygame.event.MOUSEBUTTONDOWN
        screen : pygame.Surface
        """
        x = event.pos[0]
        y = event.pos[1]
        if self.image_rect.collidepoint(x, y):
            if self.argument:
                self.func(self.argument)
            else:
                self.func()


icon = fetch_file('pictures', 'icon.jpg')  # icon for app
dgap_cat = fetch_file('pictures', 'cat_dgap.jpg')
Cat = Picture(100, 100, dgap_cat, 100, 100, angle=0)

pygame.font.init()

font = pygame.font.SysFont(None, 30)

# создание поверхностей для кнопок
button_play_surf = font.render('Play', True, 'red', 'green')
button_pause_surf = font.render('Pause', True, 'green')
button_quit_surf = font.render('Quit', True, 'red')
button_replay_surf = font.render('Retry', True, 'green')
button_sound_surf = font.render('Sound', True, 'green')
level_button_surf = []
for i in range(1, 6):
    level_button_surf.append(font.render('Level' + str(i), False, 'green',
                                         'black'))

# создание бэкграунда для главного меню и левелов
BACKGROUND = (fetch_file('pictures', 'lab_corp.png'))
BACKGROUND = pygame.transform.scale(
    BACKGROUND, (WIDTH, HEIGHT))

brick_wall = fetch_file('pictures', 'wall.png')
# создание надписи игра окончена
game_over_surf = font.render('Level Finished', True, 'green')

# созданеие инструкции
INSTRUCTIONTEXT = fetch_file('pictures', 'instruction.png')
INSTRUCTION = pygame.Surface((WIDTH, HEIGHT))
INSTRUCTION.blit(BACKGROUND, (0, 0))
INSTRUCTION.blit(INSTRUCTIONTEXT, (
    (WIDTH/2 - round(INSTRUCTIONTEXT.get_width()/2)),
    (HEIGHT/2 - round(INSTRUCTIONTEXT.get_height()/2))))
