from buttons import *
from drip import *
from ducks import *
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

# Массив с параметрами работы игры
game_state = {'finished': False,
              'paused': True,
              'in_menu': True,
              'music_banned': True,
              'shape': 'circle',
              'loaded_level': 2, 'update': 2}


def quit():
    """
    Вызов прекращает игру
    """
    game_state['finished'] = True


def go_to_menu():
    """
    Вызов переключает игру в главное меню
    Начинает трек заново
    В случае если музыка не запрещена, начинается воспроизведение
    """
    game_state['in_menu'] = True
    pygame.mixer.music.play(loops=-1)

    if game_state['music_banned']:
        pygame.mixer.music.pause()


def playpause():
    """
    Вызов контролирует паузу
    В случае если игра на паузе уберает паузу
    Иначе ставит игру на паузу
    """
    if not game_state['paused']:
        game_state['paused'] = True
    else:
        game_state['paused'] = False


def control_music():
    """
    Вызов контролирует работу музыки
    В случае если музыка не играет включает ее
    В ином случае останавливает
    """
    if not game_state['music_banned']:
        pygame.mixer.music.pause()
        game_state['music_banned'] = True
    else:
        pygame.mixer.music.unpause()
        game_state['music_banned'] = False


def control_shape():
    if game_state['shape'] == 'triangle':
        game_state['shape'] = 'circle'
    else:
        game_state['shape'] = 'triangle'


def change_level(level):
    game_state['in_menu'] = False
    game_state['update'] = level



class ButtonManager():
    play_button = Button(WIDTH / 2, HEIGHT / 2 - 300, button_play_surf,
                         playpause)

    pause_button = Button(WIDTH - 40, 30, button_pause_surf, playpause)

    quit_button = Button(WIDTH / 2, HEIGHT / 2 - 270, button_quit_surf,
                         go_to_menu)

    replay_button = Button(40, 30, button_replay_surf, change_level,
                           argument=game_state['loaded_level'])

    sound_button = Button(WIDTH - 40, HEIGHT - 30, button_sound_surf,
                          control_music)
    level_buttons = []

    for i in range(len(level_button_surf)):
        level_buttons.append(Button(WIDTH / 2 - 120 + 120 * i, HEIGHT / 2,
                                    level_button_surf[i],
                                    change_level, argument=i + 1))

    Pause_menu_buttons = [quit_button, play_button]

    Game_buttons = [pause_button, replay_button]

    Menu_buttons = level_buttons

    Menu_buttons.append(sound_button)

    @staticmethod
    def updatecurlevel(loaded_level):

        ButtonManager.replay_button = Button(40, 30, button_replay_surf,
                                             load_level, argument=loaded_level)
        # обновляем соответсвующие элементы массива
        ButtonManager.Game_buttons[1] = ButtonManager.replay_button
        # ButtonManager.Pause_menu_buttons[2] = ButtonManager.replay_button        

    @staticmethod
    def show_buttons():

        if game_state['in_menu']:
            active_buttons = ButtonManager.Menu_buttons
            pygame.mouse.set_visible(True)


        elif game_state['paused']:
            active_buttons = ButtonManager.Pause_menu_buttons
            pygame.draw.rect(screen, 'green', (round(WIDTH / 2) - 60,
                                               round(HEIGHT / 2) - 315, 120, 60), border_radius=20)
        else:
            active_buttons = ButtonManager.Game_buttons

        for button in active_buttons:
            button.draw(screen)

    @staticmethod
    def check_click():

        if game_state['in_menu']:
            active_buttons = ButtonManager.Menu_buttons

        elif game_state['paused']:
            active_buttons = ButtonManager.Pause_menu_buttons
            pygame.draw.rect(screen, 'green', (round(WIDTH / 2) - 60,
                                               round(HEIGHT / 2) - 15, 120, 60),
                             border_radius=20)
        else:

            active_buttons = ButtonManager.Game_buttons

        for button in active_buttons:
            button.check_click(event)

def load_level(level):
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


destr, destr_x, destr_y, destr_mask,indestr, indestr_x, \
indestr_y, indestr_mask, r_vector, v = load_level(game_state['update'])


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

        destr, destr_mask, r_vector, v = drip_seq(
            screen, destr, destr_x, destr_y, destr_mask,
            indestr, indestr_x, indestr_y, indestr_mask,
            r_vector, v,
            game_state['paused'], shape=game_state['shape'])

    ButtonManager.show_buttons()

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state['finished'] = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ButtonManager.check_click()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                control_shape()

pygame.quit()
print(counted_FPS)
