from buttons import *

#  dictionary with parametrs of game
game_state = {'finished': False,
              'paused': True,
              'in_menu': True,
              'show_help': True,
              'in_level_end': False,
              'in_help_menu': True,
              'music_banned': True,
              'shape': 'circle',
              'loaded_level': 1, 'update': 1}


def end_game():
    """
    Calling it stops game
    """
    game_state['finished'] = True


def go_to_menu():
    """
    Вызов переключает игру в главное меню
    Начинает трек заново
    В случае если музыка не запрещена, начинается воспроизведение
    """
    game_state['in_level_end'] = False
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
    """
    Function to control shape of cut-out area
    """

    if game_state['shape'] == 'polyhedron':
        game_state['shape'] = 'circle'
    else:
        game_state['shape'] = 'polyhedron'


def change_level(level):
    """
    Функция обновляет индикатор обновления уровня игры. Меню закрывается.
    parametrs:
    level : уровень который надо загрузить
    """
    game_state['in_menu'] = False
    game_state['update'] = level


def anounce_level_change_complete(level):
    """
    parametrs:
    level : int (1-5) загруженный уровень
    Функция обьявляет о загрузке уровня и устанавливает его как загруженный
    """

    game_state['loaded_level'] = level
    game_state['update'] = 0
    game_state['in_level_end'] = False


def anounce_level_complete():
    """
    Функция объявляет о том что уровень пройден
    """
    game_state['in_level_end'] = True


def hideshow_help():
    """
    Функция регулирует показ меню помощи
    """
    if game_state['show_help']:
        game_state['show_help'] = False
    else:
        game_state['show_help'] = True
        game_state['paused'] = True


# ниже идет описание кнопок

play_button = Button(WIDTH / 2, HEIGHT / 2 - 300, button_play_surf,
                     playpause)

pause_button = Button(WIDTH - 40, 30, button_pause_surf, playpause)

quit_button = Button(WIDTH / 2, HEIGHT / 2 - 270, button_quit_surf,
                     go_to_menu)

replay_level_button = Button(WIDTH / 2, HEIGHT / 2 - 300, button_replay_surf,
                             change_level, argument=1)

replay_button = Button(40, 30, button_replay_surf, change_level,
                       argument=1)

sound_button = Button(WIDTH - 40, HEIGHT - 30, button_sound_surf,
                      control_music)
level_buttons = []

for i in range(len(level_button_surf)):
    level_buttons.append(Button(WIDTH / 2 - 240 + 120 * i, HEIGHT / 2,
                                level_button_surf[i],
                                change_level, argument=i + 1))

Pause_menu_buttons = [quit_button, play_button]

Game_buttons = [pause_button, replay_button]

Menu_buttons = level_buttons

Menu_buttons.append(sound_button)

Level_end_buttons = [quit_button, replay_level_button]


def updatecurlevel(loaded_level):
    """
    parametrs:
    loaded_level : int (1-5) уровень который загрузили
    Эта функция обновляет  то что делает кнопка replay при загрузке уровня
    в соответствии с loaded_level
    """

    replay_button.argument = loaded_level
    replay_level_button.argument = loaded_level


def show_buttons(screen):
    """
    Рисует оконтовочки кнопок
    parametrs:
    screen : pygame.Surface
    """
    if game_state['in_menu']:
        pygame.mouse.set_visible(True)
        active_drawing_buttons = Menu_buttons

    elif game_state['paused']:
        active_drawing_buttons = Pause_menu_buttons
        pygame.draw.rect(screen, 'green', (round(WIDTH / 2) - 60,
                                           round(HEIGHT / 2) - 315, 120, 60),
                         border_radius=20)

    elif game_state['in_level_end']:
        active_drawing_buttons = Level_end_buttons
        pygame.draw.rect(screen, 'magenta', (round(WIDTH / 2) - 60,
                                             round(HEIGHT / 2) - 315, 120, 60),
                         border_radius=20)

        screen.blit(game_over_surf,
                    (round(WIDTH / 2) - round(game_over_surf.get_width() / 2),
                     40))

    else:
        active_drawing_buttons = Game_buttons

    for button in active_drawing_buttons:
        button.draw(screen)


def check_click(screen, event):
    """
    Выбирает активные кнопки и проверяет наличие нажатия
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

    elif game_state['in_level_end']:
        active_buttons = Level_end_buttons

    else:
        active_buttons = Game_buttons

    if not game_state['show_help']:
        for button in active_buttons:
            button.check_click(event)
