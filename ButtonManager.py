import pygame

from buttons import *

# Массив с параметрами работы игры
game_state = {'finished': False,
              'paused': True,
              'in_menu': True,
              'music_banned': True,
              'shape': 'circle',
              'loaded_level': 1, 'update': 1}


def end_game():
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


"""
Статический класс для работы визцализации и дейстявия всех кнопок
"""

play_button = Button(WIDTH / 2, HEIGHT / 2 - 300, button_play_surf,
                     playpause)

pause_button = Button(WIDTH - 40, 30, button_pause_surf, playpause)

quit_button = Button(WIDTH / 2, HEIGHT / 2 - 270, button_quit_surf,
                     go_to_menu)

replay_button = Button(40, 30, button_replay_surf, change_level,
                       argument=1)

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


def updatecurlevel(loaded_level):
    """
    Эта функция обновляет  то что делает кнопка replay при загрузке уровня
    """

    replay_button_new = Button(40, 30, button_replay_surf, change_level,
                               argument=loaded_level)
    # обновляем соответсвующие элементы массива
    Game_buttons[1] = replay_button_new


def show_buttons(screen):
    """
    Выбирает активные кнопки и рисует их на screen
    """
    if game_state['in_menu']:
        active_buttons = Menu_buttons
        pygame.mouse.set_visible(True)

    elif game_state['paused']:
        active_buttons = Pause_menu_buttons
        pygame.draw.rect(screen, 'green', (round(WIDTH / 2) - 60,
                                           round(HEIGHT / 2) - 315, 120, 60), border_radius=20)
    else:
        active_buttons = Game_buttons

    for button in active_buttons:
        button.draw(screen)


def check_click(screen, event):
    """
    Выберает активные кнопки и проверяет наличие нажатия
    parametrs:
    screen : pygame.screen
    event : pygame.event.MOUSEBUTTONDOWN
    """
    if game_state['in_menu']:
        active_buttons = Menu_buttons

    elif game_state['paused']:
        active_buttons = Pause_menu_buttons
        pygame.draw.rect(screen, 'green', (round(WIDTH / 2) - 60,
                                           round(HEIGHT / 2) - 15, 120, 60),
                         border_radius=20)
    else:

        active_buttons = Game_buttons

    for button in active_buttons:
        button.check_click(event)
