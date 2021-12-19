import mech
import model
import ducks
import ButtonManager
from ButtonManager import *
from ducks import *

from drip import drip_seq, Droplet
from level_config import levels

FPS = 30

pygame.display.set_icon(icon)
pygame.display.set_caption('Проект Сивухин')

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

fetch_file('music', 'machine_theme.ogg', file_type='music')
pygame.mixer.music.play()
pygame.mixer.music.pause()


def load_level(level):
    """
    parameters :
    level : int (1-5) level which needs to be loaded
    
    Returns characteristics of ground and rock
    updates Mechanisms, Ducks, water
    Announces level update, turns music off
    """

    pygame.mixer.music.fadeout(10000)

    ButtonManager.updatecurlevel(level)

    destr, destr_x, destr_y, destr_mask = levels[level - 1]['destr']()

    indestr, indestr_x, indestr_y, indestr_mask = levels[level - 1]['indestr']()
    r_vector, v = model.make_water(400, 600, -200, 0, 220)  # making water array
    # first 4 number are for border, last -amount of particles

    Duck.duck_array = levels[level - 1]['ducks']()
    mech.mech_array = levels[level - 1]['mechs']()

    Droplet.water_array = []  # destroyed all droplets

    anounce_level_change_complete(level)

    return (destr, destr_x, destr_y, destr_mask,
            indestr, indestr_x, indestr_y, indestr_mask,
            r_vector, v)


def main_loop():
    """
    Main loop of game, game is being played here
    returns :
    counted_fps : int  average frames per second in moment of game closure
    """

    #  we will announce these stuff here just in case  it will make sound stop, but it's a feature
    (destr, destr_x, destr_y, destr_mask, indestr, indestr_x,
     indestr_y, indestr_mask, r_vector, v) = load_level(game_state['update'])

    counted_fps = 0
    while not game_state['finished']:

        counted_fps = clock.get_fps()
        # if there are no ducks level is complete
        if len(Duck.duck_array) == 0:
            anounce_level_complete()

        screen.fill('white')
        # screen.blit(brick_wall, (0, 0))

        if game_state['in_menu']:
            screen.blit(BACKGROUND, (0, 0))

            # drawing collected departments
            faculties = ducks.get_faculties()
            number = 0
            while number < len(faculties):
                faculty = faculties[number]
                screen.blit(ducks.duck_image[faculty][2], (10 + 90 * number, 10))
                number += 1

        else:
            if game_state['update']:
                (destr, destr_x, destr_y, destr_mask,
                 indestr, indestr_x, indestr_y, indestr_mask,
                 r_vector, v) = load_level(game_state['update'])

            destr, r_vector, v = drip_seq(
                screen, destr, destr_x, destr_y,
                indestr, indestr_x, indestr_y,
                r_vector, v,
                game_state['paused'], shape=game_state['shape']
            )

            if game_state['in_level_end']:
                Cat.draw(screen)
                Cat.angle += 1000

        ButtonManager.show_buttons(screen)
        if game_state['show_help']:
            screen.blit(INSTRUCTION, (0, 0))

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state['finished'] = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                ButtonManager.check_click(screen, event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    control_shape()
                if event.key == pygame.K_h:
                    hideshow_help()

    return counted_fps


if __name__ == "__main__":
    print(main_loop())
    pygame.quit()
