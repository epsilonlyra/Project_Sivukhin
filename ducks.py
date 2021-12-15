import os
import json

import pygame as pg

import buttons


class Duck:
    duck_array = []

    def __init__(self, max_drop, x=-1000, y=-1000, faculty='fpmi'):
        """
        max_drop - max number of water particles consumed by the duck
        x, y - duck coordinates
        """

        self.water = 0
        self.level = 0
        self.max = max_drop
        self.x = x
        self.y = y
        self.surf = duck_image[faculty][0]
        self.mask = pg.mask.from_surface(self.surf)
        self.faculty = faculty

    def check(self, x, y, drop_mask):
        """
        x, y - duck coordinates
        Returns True if the particle hits the duck, False otherwise
        """
        x = int(x)
        y = int(y)
        offset = int(self.x) - x, int(self.y) - y
        crisis = drop_mask.overlap(self.mask, offset)
        return crisis

    def upgrade(self):
        """
        Changes level based on consumed water
        level - determines duck's stage in life
        """
        if self.water >= self.max:
            self.level = 3
        elif self.water >= 2 / 3 * self.max:
            self.level = 2
        elif self.water >= 1 / 3 * self.max:
            self.level = 1
        self.surf = duck_image[self.faculty][self.level]
        self.mask = self.mask = pg.mask.from_surface(self.surf)


def record_destroying_duck(faculty):
    """
    Records in json file the fact of duck being filled with water
    """
    with open('record.json') as file:
        data = json.load(file)
    if len(data) == 0:
        data = [faculty]
    else:
        if faculty not in data:
            data.append(faculty)
    with open('record.json', 'w') as file:
        json.dump(data, file)


def get_faculties():
    """
    Returns array of ducks from json
    """
    with open('record.json') as file:
        data = json.load(file)
    with open('record.json', 'w') as file:
        json.dump(data, file)
    return data


# creating images for the ducks
mipt = ['dgap', 'fpmi', 'faki', 'falt', 'frtk', 'fupm', 'fpfe']
duck_image = {}
for f in mipt:
    duck_image[f] = []
    for i in range(4):
        duck_pick = buttons.Picture(0, 0, buttons.fetch_file(os.path.join('pictures', 'ducks'), f + '.png'),
                                    40 + 20 * i, 40 + 20 * i)
        duck_image[f].append(duck_pick.image)
