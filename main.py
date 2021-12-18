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
    parametrs :
    level : int (1-5) уровень который мы загружаем
    
    Возращает параметры земли и неземли
    обновляет уток, воду
    Глушит музыку, объявляет о загрузке
    """

    pygame.mixer.music.fadeout(10000)

    ButtonManager.updatecurlevel(level)

    destr, destr_x, destr_y, destr_mask = levels[level - 1]['destr']()

    indestr, indestr_x, indestr_y, indestr_mask = levels[level - 1]['indestr']()
    r_vector, v = model.make_water(400, 600, -200, 0, 220)  # делаем массив воды
    # первые 4 числа определяют границы, последнее - количество частиц

    Duck.duck_array = levels[level - 1]['ducks']()

    Droplet.water_array = []  # уничтожили все капли

    anounce_level_change_complete(level)

    return (destr, destr_x, destr_y, destr_mask,
            indestr, indestr_x, indestr_y, indestr_mask,
            r_vector, v)


def main_loop():
    """
    Основной цикл игры
    returns :
    counted_fps : int  уср. количество кадров в секунду в момент закрытия
    """

    # на всякий случай обьявим их тут это заглушит музыку но это фича
    (destr, destr_x, destr_y, destr_mask, indestr, indestr_x,
     indestr_y, indestr_mask, r_vector, v) = load_level(game_state['update'])

    counted_fps = 0
    while not game_state['finished']:

        counted_fps = clock.get_fps()
        # if there are no ducs level is complete
        if len(Duck.duck_array) == 0:
            anounce_level_complete()

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
                (destr, destr_x, destr_y, destr_mask,
                 indestr, indestr_x, indestr_y, indestr_mask,
                 r_vector, v) = load_level(game_state['update'])

            destr, r_vector, v = drip_seq(
                screen, destr, destr_x, destr_y,
                indestr, indestr_x, indestr_y, indestr_mask,
                r_vector, v,
                game_state['paused'], shape=game_state['shape']
            )

            if game_state['in_level_end']:
                Cat.draw(screen)
                Cat.angle += 1000

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
    return counted_fps


if __name__ == "__main__":
    print(main_loop())
    pygame.quit()
