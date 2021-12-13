import pygame as pg
import json
import buttons
import os


class Duck:
    duck_array = []
    def __init__(self, function, max_drop, x=-1000, y=-1000, using_mask = False, faculty = 'fpmi'):
        '''
        function - функция, которая принимает координаты воды и возвращает:
        1, если частица попала в утку
        0, если частица не попала в утку
        (Т. е. function задает форму утки)
        max_drop - количество капель воды, которое должна получить утка, чтобы исчезнуть
        x, y - координаты утки
        using_mask - в случае True вместо function просто проверяется столкновение с маской
        faculty - определяет вид утки
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
        '''
        Меняет level соответственно поглощенной воде water
        level - характеристика заполненности утки водой
        '''
        if self.water >= self.max:
            self.level = 3
        elif self.water >= 2/3*self.max:
            self.level = 2
        elif self.water >= 1/3*self.max:
            self.level = 1
        self.surf = duck_image[self.faculty][self.level]
        self.mask = self.mask = pg.mask.from_surface(self.surf)


def circle_function(x_duck, y_duck, r):
    '''
    Возвращает функцию, которая возвращает 1, если x, y находятся внутри круга радиуса r
    с координатами x_duck, y_duck, и возвращает 0 иначе
    (Использовалась для создания круглой утки)
    '''
    def f(x, y):
        if (x - x_duck)**2 + (y - y_duck)**2 <= r**2:
            return True
        else:
            return False
    return f

def record_destroying_duck(faculty):
    '''
    Записывает в json файл факт спития утки вида faculty
    '''
    with open('record.json') as f:
        data = json.load(f)
    if len(data) == 0:
        data = [faculty]
    else:
        if faculty not in data:
            data.append(faculty)
    with open('record.json', 'w') as f:
        json.dump(data, f)
    

# создание картинок для уток
mipt = ['dgap', 'fpmi', 'faki', 'falt', 'frtk', 'fupm', 'fpfe']
duck_image = {}
for f in mipt:
    duck_image[f] = []
    for i in range(4):
        duck_pick = buttons.Picture(0, 0, buttons.fetch_file(os.path.join('pictures', 'ducks'), f + '.png'),
                                    40+20*i, 40+20*i)
        duck_image[f].append(duck_pick.image)







        
