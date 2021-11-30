import pygame as pg
import model
from pygame.math import Vector2
from math import atan2, degrees, pi
from buttons import fetch_file
import math



pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
BG_COLOR = pg.Color(255, 0, 0)
screen.fill(BG_COLOR)


r =15
BALL = pg.Surface((30, 30), pg.SRCALPHA)
pg.draw.circle(BALL, [250, 250, 250], [15, 15], r)
ball_pos = Vector2(30, 30)
ballrect = BALL.get_rect(center=ball_pos)
ball_vel = Vector2(0, 0)
ball_mask = pg.mask.from_surface(BALL)



WATER = pg.Surface((20, 20), pg.SRCALPHA)
r_vector, v = model.make_water(400, 600, -100, 100, 300)
pg.draw.circle(WATER, [0, 0, 255], [10, 10], 6)
drop_mask = pg.mask.from_surface(WATER)




obstacle = fetch_file('pictures', 'TEST2.png').convert_alpha()
obstacle_rect = obstacle.get_rect()
obstacle.set_colorkey((255,255,255))
ox = 350 - obstacle_rect.center[0]
oy = 250 - obstacle_rect.center[1]


body = fetch_file('pictures', 'TEST1.png').convert_alpha()
body_rect = obstacle.get_rect()
body.set_colorkey((255,255,255))
body_mask = pg.mask.from_surface(body)
ox1 = 400 - body_rect.center[0]
oy1 = 350 - body_rect.center[1]


done = False
while not done:
    r_vector, v = model.step(r_vector, v)

    #for drop in r_vector:
        
    
    #screen.fill(BG_COLOR)
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
                pg.draw.circle(obstacle, (255, 255, 255), (-ox + x, -oy + y), 50)
                print('Удаление области')
                print(pg.mouse.get_pos())
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            pg.draw.circle(obstacle, (255, 255, 255), (-ox + x, -oy + y), 0)
            print('Удаление области')
            print(pg.mouse.get_pos())
    if pg.mouse.get_pressed()[0]:
        x, y = pg.mouse.get_pos()
        pg.draw.circle(obstacle, (255, 255, 255), (-ox + x, -oy + y), 40)
        print('Удаление области')
        print(pg.mouse.get_pos())   

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


    obstacle_mask = pg.mask.from_surface(obstacle)

    offset = ox - ballrect[0], oy - ballrect[1]
    offset1 = ox1 - ballrect[0], oy1 - ballrect[1]
    '''
    for el in r_vector:
        x, y = el
        x = int(x)
        y = int(y)
        screen.blit(WATER, (x, y))
        offset2 = ox - x, oy - y
        overlap1 = drop_mask.overlap(obstacle_mask, offset2)
        if overlap1:
            ball_vel.y *= -1
            ball_vel.x *= -1'''

    overlap = ball_mask.overlap(obstacle_mask, offset) or ball_mask.overlap(body_mask, offset1) 
    

    if overlap:
        ball_vel.y *= -1
        ball_vel.x *= -1
        pg.draw.line(BALL, (0, 0, 255), (r, r), overlap)
        alp = atan2(overlap[0] - r, overlap[1] - r)
        print((alp*180/pi-90)*pi/180)

    screen.fill(BG_COLOR)
    screen.blit(BALL, ballrect)
    
    screen.blit(obstacle, (ox, oy))
    screen.blit(body, (ox1, oy1))

    for i in range(len(r_vector)):
        x, y = r_vector[i]
        x = int(x)
        y = int(y)
        screen.blit(WATER, (x, y))
        offset2 = ox - x, oy - y
        overlap1 = drop_mask.overlap(obstacle_mask, offset2)
        if overlap1:
            alpha = atan2(overlap1[0] - 10, overlap1[1] - 10)-pi/2
            #print(alpha*180/pi)
            v[i][0], v[i][1] = model.reflect(v[i][0], v[i][1], alpha)
            delta = 4.5
            r_vector[i][0] -= delta*math.cos(alpha)
            r_vector[i][1] -= delta*math.sin(alpha)
    pg.display.flip()
    clock.tick(30)

pg.quit()
