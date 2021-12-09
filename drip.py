import pygame as pg
import model
from pygame.math import Vector2
from math import atan2, degrees, pi
from buttons import fetch_file
import math
import ducks
from ducks import Duck
from ducks import duck_image



class Droplet():
    """
    Класс для отображения частиц воды
    """
    
    side = 80  # размер поверхности для капли
    water_array = []  # массив в котором хранятся следы капель
    
    def __init__(self, x, y):
        """
        Инициализация класса
        params:
        x, y - координаты центра частицы
        """
        self.x = int(x)
        self.y = int(y)
        self.r = 10 # радиус частицы
        self.surf =  pg.Surface((side, side), pg.SRCALPHA)
        pg.draw.circle(self.surf, 'blue',
                       [int(side/2), int(side/2)],
                       int(self.r))
        self.side = side
        self.k = 1 # коэфициент сжатия

    def draw(self, screen):
        
        """
        Рисует частицу и уменьшает размер поверхности
        """
        self.side = int(self.side/(self.k * self.k))
        surf = pg.transform.scale(self.surf, (self.side, self.side))
        surf.set_alpha(100)
        screen.blit(surf, (self.x, self.y))

    def draw_water(screen):
        """
        Рисует все следы из массива следов, если размер следа мал удаляет его
        """
        for drop in Droplet.water_array:
            drop.draw(screen)
            drop.k += 0.005
            if drop.k >= 1.05:
                Droplet.water_array.remove(drop)
            

def collide(mask, x_mask, y_mask, i):
    """
    Эта функция отвечает за столкновение частицы со стенками
    Она меняет скорости и координаты частиц
    mask : маска стенки
    x_mask, y_mask координаты блита  соответсвущей поверхности

    """
    global v,r_vector
    x, y = r_vector[i]
    x = int(x)
    y = int(y)
    offset2 = x_mask - x, y_mask - y
    
    crisis = drop_mask.overlap(mask, offset2)
    if crisis:
        dx = (drop_mask.overlap_area(mask, (x_mask - x + 1,
                                                 y_mask - y)) -
              drop_mask.overlap_area(mask, (x_mask - x - 1,
                                                  y_mask - y)))
        
        dy = (drop_mask.overlap_area(mask, (x_mask - x,
                                                 y_mask - y + 1)) -
              drop_mask.overlap_area(mask, (x_mask - x,
                                                  y_mask - y - 1)))
        alpha = atan2(dy, dx)
        
            
        v[i][0], v[i][1] = model.reflect(v[i][0], v[i][1], alpha)
        delta = 0.1
        while crisis: # мега костыль
            if not drop_mask.overlap(mask, offset2):
                crisis = False
                
            r_vector[i][0] += delta*math.cos(alpha)
            r_vector[i][1] += delta*math.sin(alpha)
            
            x, y = r_vector[i]
            x = int(x)
            y = int(y)
            
            offset2 = x_mask- x, y_mask - y


def get_obstacles(image, x, y):
    """
    Возвращает параметры для препятствия с картинки,
    parametrs:
    image - поверхность Pygame
    x y - координаты центра соотв. прямоугольника
    """
    image = image.convert_alpha()
    image_rect = image.get_rect(center = (x, y))
    image.set_colorkey('white')
    image_x = image_rect[0]
    image_y = image_rect[1]
    image_mask = pg.mask.from_surface(image)
    return(image, image_x, image_y, image_mask)

def cut_out(Pressed, position, surface, surface_x, surface_y):
    """
    Вырезаем область
    """
    r = 40
    if Pressed: # если мышь зажата удаляет область
            x, y = position
            pg.draw.circle(surface, 'white', (-surface_x + x,
                                           -surface_y + y), r)
    

pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
BG_COLOR = pg.Color(255, 0, 0)
screen.fill(BG_COLOR)

# создание маски для частицы воды(общая для всех)
side = 20
WATER = pg.Surface((side, side), pg.SRCALPHA)
r_vector, v = model.make_water(400, 600, -200, 0, 300)
r_water = 4
pg.draw.circle(WATER, [0, 0, 255], [int(side/2), int(side/2)], r_water)
drop_mask = pg.mask.from_surface(WATER)

def drip_sequance():
    """
    
    Эта функция должна принимать уток, поверхности земли и трубы
    Она вставляется в основной цикл maina
    Сделать избавиться от всех глобалов в dripe
    """
    pass
    
    
    
def example():
    global r_vector, v, a
    
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    BG_COLOR = pg.Color(255, 0, 0)
    screen.fill(BG_COLOR)

    destr, destr_x, destr_y, destr_mask = get_obstacles(
        fetch_file('pictures', 'TEST2.png','TEST'), 340, 240)
    
    indestr, indestr_x, indestr_y, indestr_mask = get_obstacles(
        fetch_file('pictures', 'TEST1.png','TEST'), 340, 440)

    # шар теста
    r = 15
    BALL = pg.Surface((30, 30), pg.SRCALPHA)
    pg.draw.circle(BALL, [250, 250, 250], [15, 15], r)
    ball_pos = Vector2(30, 30)
    ballrect = BALL.get_rect(center=ball_pos)
    ball_vel = Vector2(0, 0)
    ball_mask = pg.mask.from_surface(BALL)
    
    done = False
    pause = False

    # инициализация уток
        
    Duck.duck_array.append(Duck(ducks.circle_function(200, 200, 10), 30, 200, 200,
                           using_mask = True))
    while not done:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                # контроль мяча
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    ball_vel.x = -5
                elif event.key == pg.K_d:
                    ball_vel.x = 5
                elif event.key == pg.K_w:
                    ball_vel.y = -5
                elif event.key == pg.K_s:
                     ball_vel.y = 5
                elif event.key == pg.K_z: # удаления по кнопке
                    x, y = pg.mouse.get_pos()
                    pg.draw.circle(destr, (255, 255, 255),
                                   (-destr_x + x, destr_y + y), 50)

        cut_out(pg.mouse.get_pressed()[0], pg.mouse.get_pos(),
                destr, destr_x, destr_y)
        
        # работа с мячом
        ball_vel *= .94
        ball_pos += ball_vel
        ballrect.center = ball_pos
        
        if ballrect.top < 0 and ball_vel.y < 0:
            ball_vel.y *= -1
        elif ballrect.bottom > screen.get_height() and ball_vel.y > 0:
            ball_vel.y *= -1
        if ballrect.left < 0 and ball_vel.x < 0:
            ball_vel.x *= -1
        elif ballrect.right > screen.get_width() and ball_vel.x > 0:
            ball_vel.x *= -1
        


        

        offset = destr_x - ballrect[0], destr_y - ballrect[1]
        offset1 = indestr_x - ballrect[0], indestr_y - ballrect[1]

        overlap = (ball_mask.overlap(destr_mask, offset) or
                   ball_mask.overlap(indestr_mask, offset1))
        
        if overlap:
            ball_vel.y *= -1
            ball_vel.x *= -1
            pg.draw.line(BALL, (0, 0, 255), (r, r), overlap)
            alp = atan2(overlap[0] - r, overlap[1] - r)
            print((alp*180/pi-90)*pi/180)

        screen.fill(BG_COLOR)
        if not pause:
            r_vector, v = model.step(r_vector, v) # работа модели
        
        
        destr_mask = pg.mask.from_surface(destr)
        # движение воды и работа с утками
        for i in range(len(r_vector)):
            
            x, y = r_vector[i]
            Droplet.water_array.append(Droplet(x,y)) # добавляем новую поз.

            # соударения с поверхностями
            collide(destr_mask, destr_x, destr_y, i)
            collide(indestr_mask, indestr_x, indestr_y, i)

            for d in Duck.duck_array: # проверяем столновения с утками
                if d.check(x, y, drop_mask):
                    d.water += 1
                    r_vector[i] = [-1000, -1000] # cсылаем в Сибирь
                    break

        # обновление уток
        for d in Duck.duck_array:
            d.upgrade()
            if d.level == 3:
                Duck.duck_array.remove(d)

        Droplet.draw_water(screen) # рисуем воду

        # рисуем землю и неземлю
        screen.blit(destr, (destr_x, destr_y))
        screen.blit(indestr, (indestr_x, indestr_y))

        for d in Duck.duck_array: # рисуем уток
                screen.blit(duck_image[d.level], (int(d.x), int(d.y)))

        screen.blit(BALL, ballrect) # рисуем мяч

        pg.display.flip()
        clock.tick(30)
        a = (clock.get_fps())

if __name__ == "__main__":
    example()
    print(a)
    pg.quit()



