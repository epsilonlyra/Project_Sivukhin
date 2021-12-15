import math
import random
from math import atan2, pi

import pygame as pg
from pygame.math import Vector2

import ducks
import model
from buttons import fetch_file
from ducks import Duck
from ducks import duck_image


def draw_polygon(screen, x, y):
    """
    Draws a white polygon on screen
    x, y - coordinates of the polygon (not sure which point exactly)
    """

    n = random.randint(4, 6)
    angles_array = [(2 * i * math.pi / n) + random.randrange(-7, 7, 1) / 100 for i in range(n)]
    points = []
    for angle in angles_array:
        length = 30 + random.randint(-4, 4)
        points.append((x + length * math.sin(angle),
                       y - length * math.cos(angle)))
    pg.draw.polygon(screen, 'white', points)


class Droplet:
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
        self.r = 10  # радиус частицы
        self.surf = pg.Surface((side, side), pg.SRCALPHA)
        pg.draw.circle(self.surf, 'blue',
                       [int(side / 2), int(side / 2)],
                       int(self.r))
        self.side = side
        self.k = 1  # коэфициент сжатия

    def draw(self, screen, paused):

        """
        Рисует частицу и уменьшает размер поверхности
        """
        if not paused:
            self.side = int(self.side / (self.k * self.k))

        surf = pg.transform.scale(self.surf, (self.side, self.side))
        surf.set_alpha(100)
        screen.blit(surf, (self.x, self.y))

    @staticmethod
    def draw_water(screen, paused):
        """
        Рисует все следы из массива следов, если размер следа мал удаляет его
        """
        if not paused:
            for drop in Droplet.water_array:
                drop.draw(screen, paused)
                drop.k += 0.005
                if drop.k >= 1.05:
                    Droplet.water_array.remove(drop)
        else:
            for drop in Droplet.water_array:
                drop.draw(screen, paused)


def collide(mask, x_mask, y_mask, r_vector, i, v):
    """
    Эта функция отвечает за столкновение частицы со стенками
    Она меняет скорости и координаты частиц
    mask : маска стенки
    x_mask, y_mask координаты блита  соответсвущей поверхности

    """
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
        while crisis:  # мега костыль
            if not drop_mask.overlap(mask, offset2):
                crisis = False

            r_vector[i][0] += delta * math.cos(alpha)
            r_vector[i][1] += delta * math.sin(alpha)

            x, y = r_vector[i]
            x = int(x)
            y = int(y)

            offset2 = x_mask - x, y_mask - y
    return r_vector[i], v[i][0], v[i][1]


def get_obstacles(image, x, y):
    """
    Возвращает параметры для препятствия с картинки,
    parametrs:
    image - поверхность Pygame
    x y - координаты центра соотв. прямоугольника
    """
    image = image.convert_alpha()
    image_rect = image.get_rect(center=(x, y))
    image.set_colorkey('white')
    image_x = image_rect[0]
    image_y = image_rect[1]
    image_mask = pg.mask.from_surface(image)
    return image, image_x, image_y, image_mask


def cut_out(pressed_down, position, surface, surface_x, surface_y, shape='circle'):
    """
    Вырезаем область
    """
    r = 40
    if pressed_down:  # если мышь зажата удаляет область
        x, y = position
        if shape == 'triangle':
            draw_polygon(surface, -surface_x + x, surface_y + y)

        if shape == 'circle':
            pg.draw.circle(surface, 'white', (-surface_x + x,
                                              -surface_y + y), r)


# создание маски для частицы воды(общая для всех)
side = 20
WATER = pg.Surface((side, side), pg.SRCALPHA)
r_water = 4
pg.draw.circle(WATER, [0, 0, 255], [int(side / 2), int(side / 2)], r_water)
drop_mask = pg.mask.from_surface(WATER)

shovel = fetch_file('pictures', 'lop.png')
none = fetch_file('pictures', 'none.png')
shovel.set_colorkey('white')
none.set_colorkey('white')


def drip_seq(screen,
             destr, destr_x, destr_y, indestr,
             indestr_x, indestr_y, indestr_mask,
             r_vector, v,
             paused,
             shape='circle'):
    """
    Это квинтиссенция всего что делает drip
    parametrs:
    
    """

    destr_mask = pg.mask.from_surface(destr)
    mx, my = pg.mouse.get_pos()
    if not paused:
        r_vector, v = model.step(r_vector, v)  # работа модели
        cut_out(pg.mouse.get_pressed()[0], (mx, my), destr,
                destr_x, destr_y, shape=shape)

    # движение воды и работа с утками

    for i in range(len(r_vector)):
        x, y = r_vector[i]
        if not paused:
            Droplet.water_array.append(Droplet(x, y))  # добавляем новую поз.

        # соударения с поверхностями
        collide(destr_mask, destr_x, destr_y, r_vector, i, v)
        collide(indestr_mask, indestr_x, indestr_y, r_vector, i, v)

        for d in Duck.duck_array:  # проверяем столновения с утками
            if d.check(x, y, drop_mask):
                d.water += 1
                r_vector[i] = [-1000, -1000]  # cсылаем в Сибирь
                break

    # обновление уток
    for d in Duck.duck_array:
        d.upgrade()
        if d.level == 3:
            Duck.duck_array.remove(d)
            ducks.record_destroying_duck(d.faculty)

    mouse = none
    # здесь возможен выход за границы маски

    try:
        is_on_destr = destr_mask.get_at((mx - destr_x, my - destr_y))
    except IndexError:
        is_on_destr = 0

    try:
        is_on_indestr = indestr_mask.get_at((mx - indestr_x, my - indestr_y))
    except IndexError:
        is_on_indestr = 0

    mouse_skin_change = (is_on_destr and (not is_on_indestr))

    if not paused:
        if mouse_skin_change:
            pg.mouse.set_visible(False)
            mouse = shovel
        else:
            pg.mouse.set_visible(True)

    Droplet.draw_water(screen, paused)  # рисуем воду

    # рисуем землю и неземлю
    screen.blit(destr, (destr_x, destr_y))
    screen.blit(indestr, (indestr_x, indestr_y))

    # рисуем мышь
    screen.blit(mouse, (mx, my - mouse.get_height()))

    for d in Duck.duck_array:  # рисуем уток
        screen.blit(duck_image[d.faculty][d.level], (int(d.x), int(d.y)))

    return destr, r_vector, v


def example():
    fps = 0
    paused = False
    r_vector, v = model.make_water(400, 600, -200, 0, 30)  # делаем массив воды

    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    bg_color = pg.Color(255, 0, 0)
    screen.fill(bg_color)

    destr, destr_x, destr_y, destr_mask = get_obstacles(
        fetch_file('pictures', 'TEST2.png', 'TEST'), 340, 240)

    indestr, indestr_x, indestr_y, indestr_mask = get_obstacles(
        fetch_file('pictures', 'TEST1.png', 'TEST'), 340, 440)

    # шар теста
    r = 15
    ball = pg.Surface((30, 30), pg.SRCALPHA)
    pg.draw.circle(ball, [250, 250, 250], [15, 15], r)
    ball_pos = Vector2(30, 30)
    ballrect = ball.get_rect(center=ball_pos)
    ball_vel = Vector2(0, 0)
    ball_mask = pg.mask.from_surface(ball)

    done = False

    # инициализация уток

    Duck.duck_array.append(Duck(30, 200, 200,))
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
                elif event.key == pg.K_z:  # удаления по кнопке
                    x, y = pg.mouse.get_pos()
                    draw_polygon(destr, -destr_x + x, destr_y + y)

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
            pg.draw.line(ball, (0, 0, 255), (r, r), overlap)
            alp = atan2(overlap[0] - r, overlap[1] - r)
            print((alp * 180 / pi - 90) * pi / 180)

        screen.fill(bg_color)
        destr, r_vector, v = drip_seq(
            screen, destr, destr_x, destr_y, indestr, indestr_x, indestr_y, indestr_mask,
            r_vector, v,
            paused)
        screen.blit(ball, ballrect)  # рисуем мяч

        pg.display.flip()
        clock.tick(30)
        fps = (clock.get_fps())
    return fps


if __name__ == "__main__":
    FPS = example()
    print(FPS)
    pg.quit()
