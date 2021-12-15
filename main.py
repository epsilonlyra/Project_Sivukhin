import model
import ducks
import ButtonManager
from ButtonManager import *
from ducks import *

from drip import drip_seq, Droplet
from level_config import levels

WIDTH = 700
HEIGHT = 800
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
    Возращает параметры земли и неземли обновляет уток
    """
    
    game_state['loaded_level'] = level

    game_state['update'] = 0

    pygame.mixer.music.fadeout(10000)

    ButtonManager.updatecurlevel(level)

    destr, destr_x, destr_y, destr_mask = levels[level - 1]['destr']()

    indestr, indestr_x, indestr_y, indestr_mask = levels[level - 1]['indestr']()

    r_vector, v = model.make_water(400, 600, -200, 0, 220)  # делаем массив воды
    # первые 4 числа определяют границы, последнее - количество частиц

    Duck.duck_array = levels[level - 1]['ducks']()

    Droplet.water_array = []  # уничтожили все капли

    return (destr, destr_x, destr_y, destr_mask,
            indestr, indestr_x, indestr_y, indestr_mask,
            r_vector, v)


# на всякий случай обьявим их тут это заглушит музыку но это фича
destr, destr_x, destr_y, destr_mask, indestr, indestr_x, \
    indestr_y, indestr_mask, r_vector, v = load_level(game_state['update'])

def main_loop():
    """
    Основной цикл игры
    """
    
    counted_FPS = 0
    while not game_state['finished']:
        counted_FPS = clock.get_fps()

        screen.fill('white')
        # screen.blit(brick_wall, (0, 0))

        if game_state['in_menu']:
            screen.blit(BACKGROUND, (0, 0))

            # рисуем собранные факультеты
            faculties = ducks.get_faculties()
            i = 0
            while i < len(faculties):
                f = faculties[i]
                screen.blit(ducks.duck_image[f][2], (10 + 90 * i, 10))
                i += 1

        else:
            if game_state['update']:
                destr, destr_x, destr_y, destr_mask, \
                    indestr, indestr_x, indestr_y, indestr_mask, \
                    r_vector, v = load_level(game_state['update'])

            destr, r_vector, v = drip_seq(
                screen, destr, destr_x, destr_y,
                indestr, indestr_x, indestr_y, indestr_mask,
                r_vector, v,
                game_state['paused'], shape=game_state['shape']
            )

        ButtonManager.show_buttons(screen)

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
    return counted_FPS
    
if __name__ == "__main__":
    print(main_loop())
    pygame.quit()
