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
import mech


def draw_polygon(screen, x, y):
    """
    Draws a white polygon on screen
    parameters:
    x, y : int coordinates of some point of the polygon
    screen : pygame.Surface
    """

    n = random.randint(3, 6)
    angles_array = [(2 * i * math.pi / n) + random.randrange(-7, 7, 1) / 100 for i in range(n)]
    points = []
    for angle in angles_array:
        length = 30 + random.randint(-10, 10)
        points.append((x + length * math.sin(angle),
                       y + length * math.cos(angle)))
    pg.draw.polygon(screen, 'white', points)


class Droplet:
    side = 30  # size of droplet surface
    water_array = []  # list in which we hold water to draw

    def __init__(self, x, y):
        """
        Initialise  class for water visualization
        params:
        x, y - coordinates of particle center
        """
        self.x = int(x)
        self.y = int(y)
        self.r = 10  # particle radius
        self.surf = pg.Surface((side, side), pg.SRCALPHA)
        self.surf.set_alpha(100)
        pg.draw.circle(self.surf, 'blue',
                       [int(side / 2), int(side / 2)],
                       int(self.r))
        self.side = side
        self.compression = 1  # coefficient for compression
        self.time = 0

    def draw(self, screen, paused):

        """
        Draws particle and compresses it
        params:
        screen : pygame.Surface
        paused : Boolean : is game paused
        """

        surf = pg.transform.scale(self.surf, (self.side, self.side))
        screen.blit(surf, (self.x, self.y))
        if not paused:
            self.side = int(self.side / self.compression)

    @staticmethod
    def draw_water(screen, paused):
        """
        parameters:
        screen : pygame.Surface s
        paused : Boolean is game paused
        Draws all traces from the trace list, if trace is small it gets exterminated
        """
        for drop in Droplet.water_array:
            drop.draw(screen, paused)
        if not paused:
            for drop in Droplet.water_array:
                drop.compression += 0.001
                drop.time += 1
                if drop.time >= 10:
                    Droplet.water_array.remove(drop)


def collide(mask, x_mask, y_mask, r_vector, i, v):
    """
    This function is responsible for collisions of particle with ground
    It changed velocity and position

    parameters:
    mask : pg.Mask of ground
    x_mask, y_mask : coordinates of ground blit
    r_vector : np array holding coordinates of particle
    i : number of particle
    v : np array holding velocities
    
    returns:
    r_vector[i], v[i][0], v[i][1] : params of particle after reflection
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

        # when particle is stuck it begins quantum movement from obstacle
        move_quant = 0.1  # quant of movement 
        while crisis:  # super stupid
            if not drop_mask.overlap(mask, offset2):
                crisis = False

            r_vector[i][0] += move_quant * math.cos(alpha)
            r_vector[i][1] += move_quant * math.sin(alpha)

            x, y = r_vector[i]
            x = int(x)
            y = int(y)

            offset2 = x_mask - x, y_mask - y
    return r_vector[i], v[i][0], v[i][1]


def get_obstacles(image, x, y):
    """
    Returns params for obstacle from picture
    parameters:
    image - Pygame.Surface
    x y - coordinates of center of corresponding rectangle
    """
    image = image.convert_alpha()
    image_rect = image.get_rect(center=(x, y))
    image.set_colorkey('white')
    image_x = image_rect[0]
    image_y = image_rect[1]
    image_mask = pg.mask.from_surface(image)
    return image, image_x, image_y, image_mask


def cut_out(pressed_down, position, surface, surface_x, surface_y,
            shape='circle'):
    """
    Cutting out shape
    """
    r = 40
    if pressed_down:  # if mouse button is down
        x, y = position
        if shape == 'polyhedron':
            if pg.mouse.get_rel() != (0, 0):
                draw_polygon(surface, -surface_x + x, -surface_y + y)

        if shape == 'circle':
            pg.draw.circle(surface, 'white', (-surface_x + x,
                                              -surface_y + y), r)


#  create mask for water particle (one for all)
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
             destr, destr_x, destr_y, indestr_original,
             indestr_x, indestr_y, r_vector, v,
             paused,
             shape='circle'):
    """
    Function that processes game
    parametrs:
    destr, indestr : pygame.Surface represents destructible and indestructible
    destr_x, destr_y, indestr_x, indestr_y : int coordinates of left corner \
        corresponding rectum
    r_vector, v : numpy arrays holding position and speed of water particles
    paused : Boolean is the game on pause
    shape : 'circle' or 'polyhedron' cut-out area type
    
    returns:
    destr : pygame.Surface destructible ground after cutting out hole
    r_vector, v : changed numpy arrays holding info about particles after\
        in-game tick
    """

    # creating a copy of indestr so that mechanism are not permanently drawn
    indestr = indestr_original.copy()

    # adding mechanisms to indestr
    for mechanism in mech.mech_array:
        mechanism.draw(indestr)
    indestr_mask = pg.mask.from_surface(indestr)

    destr_mask = pg.mask.from_surface(destr)
    mx, my = pg.mouse.get_pos()
    if not paused:
        # moving mechanisms
        for mechanism in mech.mech_array:
            mechanism.move()

        r_vector, v = model.step(r_vector, v)  # model at work
        cut_out(pg.mouse.get_pressed()[0], (mx, my), destr,
                destr_x, destr_y, shape=shape)

    # add new trace
    for i in range(len(r_vector)):
        x, y = r_vector[i]
        if not paused:
            Droplet.water_array.append(Droplet(x, y))

        # checking collision with collector
        for mechanism in mech.mech_array:
            if not mechanism.got_water:
                if mechanism.check_collision_with_collector(x - indestr_x, y - indestr_y, drop_mask):
                    mechanism.collected_water()
                    r_vector[i] = [-1000, 1000]

        # сollision with surfaces
        collide(destr_mask, destr_x, destr_y, r_vector, i, v)
        collide(indestr_mask, indestr_x, indestr_y, r_vector, i, v)

        for d in Duck.duck_array:  # collision with Ducks
            if d.check(x, y, drop_mask):
                d.water += 1
                r_vector[i] = [-1000, -1000]  # send to Siberia
                break

    # update Ducks
    for d in Duck.duck_array:
        d.upgrade()
        if d.level == 3:
            Duck.duck_array.remove(d)
            ducks.record_destroying_duck(d.faculty)

    mouse = none
    # it is possible to get out of mask borders here

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

    Droplet.draw_water(screen, paused)  # drawing water

    # drawing ground and rock
    screen.blit(destr, (destr_x, destr_y))
    screen.blit(indestr, (indestr_x, indestr_y))

    # drawing mouse
    screen.blit(mouse, (mx, my - mouse.get_height()))

    # drawing ducks
    for d in Duck.duck_array:
        screen.blit(duck_image[d.faculty][d.level], (int(d.x), int(d.y)))

    return destr, r_vector, v


def example():
    """
    example for demonstrating drip.py module abilities
    includes a movable  by W,A,S,D ball
    
    returns:
    fps : float average frames per sec. at the closure of the prog
    """
    fps = 0
    paused = False
    r_vector, v = model.make_water(400, 600, -200, 0, 30)  # create water array

    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    bg_color = pg.Color(255, 0, 0)
    screen.fill(bg_color)

    destr, destr_x, destr_y, destr_mask = get_obstacles(
        fetch_file('pictures', 'TEST2.png', 'TEST'), 340, 240)

    indestr, indestr_x, indestr_y, indestr_mask = get_obstacles(
        fetch_file('pictures', 'TEST1.png', 'TEST'), 340, 440)

    # test ball
    r = 15
    ball = pg.Surface((30, 30), pg.SRCALPHA)
    pg.draw.circle(ball, [250, 250, 250], [15, 15], r)
    ball_pos = Vector2(30, 30)
    ballrect = ball.get_rect(center=ball_pos)
    ball_vel = Vector2(0, 0)
    ball_mask = pg.mask.from_surface(ball)

    done = False

    # Duck init

    Duck.duck_array.append(Duck(30, 200, 200, ))
    while not done:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                # ball control
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    ball_vel.x = -5
                elif event.key == pg.K_d:
                    ball_vel.x = 5
                elif event.key == pg.K_w:
                    ball_vel.y = -5
                elif event.key == pg.K_s:
                    ball_vel.y = 5
                elif event.key == pg.K_z:  # delete if Z pressed
                    x, y = pg.mouse.get_pos()
                    draw_polygon(destr, -destr_x + x, destr_y + y)

        # work with ball
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
        destr_mask = pg.mask.from_surface(destr)
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
            screen, destr, destr_x, destr_y,
            indestr, indestr_x, indestr_y,
            r_vector, v,
            paused)
        screen.blit(ball, ballrect)  # drawing ball

        pg.display.flip()
        clock.tick(30)
        fps = (clock.get_fps())
    return fps


if __name__ == "__main__":
    FPS = example()
    print(FPS)
    pg.quit()
