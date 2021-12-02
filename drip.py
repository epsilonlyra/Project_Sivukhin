import pygame as pg
import model
from pygame.math import Vector2
from math import atan2, degrees, pi
from buttons import fetch_file
import math

def collide(mask, x_mask, y_mask, i):
    """
    Эта функция отвечает за столкновение частицы со стенками
    Она меняет скорости и координаты частиц
    mask : маска стенки
    x_mask, y_mask координаты блита  соответсвущей поверхности

    """
    global v,r_vector
    x, y = r_vector[i]
    offset2 = x_mask- x, y_mask - y
    
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
        while crisis:
            if not drop_mask.overlap(mask, offset2):
                crisis = False
            r_vector[i][0] += delta*math.cos(alpha)
            r_vector[i][1] += delta*math.sin(alpha)
            x, y = r_vector[i]
            offset2 = x_mask- x, y_mask - y


def get_obstacles(image, x, y):
    image = image.convert_alpha()
    image_rect = image.get_rect(center = (x, y))
    image.set_colorkey('white')
    image_x = image_rect[0]
    image_y = image_rect[1]
    image_mask = pg.mask.from_surface(image)
    return(image, image_x, image_y, image_mask)
    
    

pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
BG_COLOR = pg.Color(255, 0, 0)
screen.fill(BG_COLOR)

side = 20
WATER = pg.Surface((side, side), pg.SRCALPHA)
r_vector, v = model.make_water(400, 600, -200, 0, 300)
r_water = 6
pg.draw.circle(WATER, [0, 0, 255], [int(side/2), int(side/2)], r_water)
drop_mask = pg.mask.from_surface(WATER)


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
    
    r = 15
    BALL = pg.Surface((30, 30), pg.SRCALPHA)
    pg.draw.circle(BALL, [250, 250, 250], [15, 15], r)
    ball_pos = Vector2(30, 30)
    ballrect = BALL.get_rect(center=ball_pos)
    ball_vel = Vector2(0, 0)
    ball_mask = pg.mask.from_surface(BALL)
    
    done = False
    while not done:
        r_vector, v = model.step(r_vector, v)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    ball_vel.x = -5
                elif event.key == pg.K_d:
                    ball_vel.x = 5
                elif event.key == pg.K_w:
                    ball_vel.y = -5
                elif event.key == pg.K_s:
                     ball_vel.y = 5
                elif event.key == pg.K_z:
                    x, y = pg.mouse.get_pos()
                    pg.draw.circle(destr, (255, 255, 255),
                                   (-destr_x + x, destr_y + y), 50)
                    #print('Удаление области')
                    #print(pg.mouse.get_pos())"""
                #print('Удаление области')
                #print(pg.mouse.get_pos())
        if pg.mouse.get_pressed()[0]:
            x, y = pg.mouse.get_pos()
            pg.draw.circle(destr, (255, 255, 255), (-destr_x + x,
                                                    -destr_y + y), 40)
            #print('Удаление области')
            #print(pg.mouse.get_pos())

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
        


        destr_mask = pg.mask.from_surface(destr)

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
        screen.blit(BALL, ballrect)
        
        screen.blit(destr, (destr_x, destr_y))
        screen.blit(indestr, (indestr_x, indestr_y))

        for i in range(len(r_vector)):
            x, y = r_vector[i]
            screen.blit(WATER, (int(x), int(y)))
            
            collide(destr_mask, destr_x, destr_y, i)
            collide(indestr_mask, indestr_x, indestr_y, i)
            
                    
        pg.display.flip()
        clock.tick(30)
        a = (clock.get_fps())

if __name__ == "__main__":
    example()
print(a)

pg.quit()

