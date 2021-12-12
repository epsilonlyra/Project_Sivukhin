import pygame as pg
import buttons



class Duck:
    duck_array = []
    def __init__(self, function, max_drop, x=-1000, y=-1000, using_mask = False, faculty = 'fpmi'):
        '''
        function - функция, которая принимает координаты воды и возвращает
        1, если частица попала в утку
        0, если частица не попала в утку
        Т. е. function задает форму утки

        max_drop - количество капель воды, которое должна получить утка, чтобы исчезнуть
        '''
        
        self.water = 0
        self.level = 0
        self.func = function
        self.max = max_drop
        self.x = x
        self.y = y
        self.surf = duck_image[faculty][0]
        self.mask = pg.mask.from_surface(self.surf)
        self.using_mask = using_mask
        self.faculty = faculty
        
                                         
    def check(self, x, y, drop_mask):
        '''
        x, y - координаты частицы
        Возвращает True, если частица попала в утку, False - иначе
        '''
        if self.using_mask:
            x = int(x)
            y = int(y)
            offset = int(self.x) - x, int(self.y) - y
            crisis = drop_mask.overlap(self.mask, offset)
            return crisis
        else:
            return self.func(x, y)

    def upgrade(self):
        if self.water >= self.max:
            self.level = 3
        elif self.water >= 2/3*self.max:
            self.level = 2
        elif self.water >= 1/3*self.max:
            self.level = 1
        self.surf = duck_image[self.faculty][self.level]
        self.mask = self.mask = pg.mask.from_surface(self.surf)


def circle_function(x_duck, y_duck, r):
    def f(x, y):
        if (x - x_duck)**2 + (y - y_duck)**2 <= r**2:
            return True
        else:
            return False
    return f

side = 40
r = 10
mipt = ['dgap', 'fpmi']
duck_image = {}
for f in mipt:
    duck_image[f] = []
    for i in range(4):
        duck_pick = buttons.Picture(0, 0, buttons.fetch_file('pictures', f+'.png'),
                                    40+20*i, 40+20*i)
        duck_image[f].append(duck_pick.image)




        
