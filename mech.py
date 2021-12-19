import os

import pygame

import buttons


class Mech:
    def __init__(self, collector_x, collector_y, collector_angle, body_x, body_y, body_angle, color):
        """
        Collector - part of the mech that collects water
        Body - part that moves after collector receives water

        collector_x, collector_y, collector_angle - parameters, determining position of collector
        body_x, body_y, body_angle - parameters, determining position of body
        color - color of the body and collector, either 'orange' or 'blue' ('blue' not added yet)
        """
        self.color = color

        self.collector_x = collector_x
        self.collector_y = collector_y
        self.collector_angle = collector_angle
        self.collector_surf = pygame.transform.rotate(images['collector_' + self.color], self.collector_angle)
        self.collector_mask = pygame.mask.from_surface(self.collector_surf)

        self.body_x = body_x
        self.body_y = body_y
        self.body_angle = body_angle
        self.body_surf = pygame.transform.rotate(images['body_' + self.color], self.body_angle)
        self.body_mask = pygame.mask.from_surface(self.body_surf)

        self.state = 0
        self.got_water = False

    def check_collision_with_collector(self, x, y, drop_mask):
        """
        Returns True if particle at x, y collides with collector, False otherwise
        """
        x = int(x)
        y = int(y)
        offset = int(self.collector_x) - x, int(self.collector_y) - y
        intersections = drop_mask.overlap(self.collector_mask, offset)
        overlap = False
        if intersections:
            overlap = True
        return overlap

    def draw(self, screen, x=0, y=0):
        """
        Draws collector and body on the screen, displaced by x, y
        """
        screen.blit(self.collector_surf, (int(self.collector_x) + int(x), int(self.collector_y) + int(y)))
        screen.blit(self.body_surf, (int(self.body_x) + int(x), int(self.body_y) + int(y)))

    def collected_water(self):
        """
        Turns on got_water so that the body will start moving
        """
        self.got_water = True

    def move(self):
        """
        Moves body if needed
        """
        if self.got_water:
            if self.state < 100:
                self.state += 1
                self.body_x += 1


# creating array for Mech objects
mech_array = []

# creating images for mechanisms
collectors = ['collector_orange']
bodies = ['body_orange']
images = {}
for col in collectors:
    picture = buttons.Picture(0, 0, buttons.fetch_file(os.path.join('pictures', 'mechanisms'), col + '.png'),
                              40, 50)
    images[col] = picture.image

for body in bodies:
    picture = buttons.Picture(0, 0, buttons.fetch_file(os.path.join('pictures', 'mechanisms'), body + '.png'),
                              120, 40)
    images[body] = picture.image
