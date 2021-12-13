import pygame
from pygame.draw import *
from buttons import *
import drip
import model
from drip import drip_seq, get_obstacles, Droplet
import ducks
from ducks import *
import level_config
from level_config import *

WIDTH = 700
HEIGHT = 800
FPS = 30

pygame.display.set_icon(icon)
pygame.display.set_caption(('Проект Сивухин'))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mixer.init
fetch_file('music','machine_theme.ogg', type = 'music')
pygame.mixer.music.play()
pygame.mixer.music.pause()

finished = False
paused = True
in_menu = True
music_banned = True

loaded_level = 2
   
def quit():
    global finished
    finished = True

def go_to_menu():
    global in_menu
    
    in_menu = True
    
    pygame.mixer.music.play(loops = -1)
    if music_banned:
        pygame.mixer.music.pause()

def playpause():
    global paused
    if not paused:
        paused = True
    else:
        paused = False

def control_music():
    global music_banned
    if not music_banned:
        pygame.mixer.music.pause()
        music_banned = True
    else:
        pygame.mixer.music.unpause()
        music_banned = False

shape = 'circle'

def control_shape():
    global shape
        
    if shape == None:
        shape ='circle'
    else:
        shape = None

def load_level(level):
    
    global destr, destr_x, destr_y, destr_mask, \
    indestr, indestr_x, indestr_y, indestr_mask, \
    r_vector, v,\
    in_menu, \
    ButMan

    in_menu = False
    pygame.mixer.music.fadeout(10000)

    ButtonManager.updatecurlevel(level)
   
    destr, destr_x, destr_y, destr_mask = levels[level-1]['destr']()

    indestr, indestr_x, indestr_y, indestr_mask = levels[level-1]['indestr']()
    
    r_vector, v = model.make_water(400, 600, -200, 0, 220) # делаем массив воды
    # первые 4 числа определяют границы, последнее - количество частиц

    Duck.duck_array = levels[level-1]['ducks']()
    
    Droplet.water_array = [] # уничтожили все капли


class ButtonManager():

    play_button =  Button(WIDTH / 2, HEIGHT /  2 - 300, button_play_surf, playpause)
    pause_button =  Button(WIDTH - 40, 30 , button_pause_surf, playpause)
    quit_button = Button(WIDTH / 2, HEIGHT /  2 - 270, button_quit_surf,
                         go_to_menu)
    replay_button = Button(40, 30, button_replay_surf, load_level,
                           argument=loaded_level)
    sound_button =  Button(WIDTH - 40, HEIGHT - 30 , button_sound_surf,
                           control_music)
    level_buttons = []
    for i in range(len(level_button_surf)):
        level_buttons.append(Button(WIDTH / 2 - 120 + 120 * i, HEIGHT /  2,
                              level_button_surf[i],
                              load_level, argument=i+1))
    
    Pause_menu_buttons = [quit_button, play_button]
    Game_buttons = [pause_button, replay_button]
    Menu_buttons = level_buttons
    Menu_buttons.append(sound_button)
    
    def updatecurlevel(loaded_level):
        ButtonManager.replay_button = Button(40, 30, button_replay_surf,
                                             load_level, argument=loaded_level)
        # обновляем соответсвующие элементы массива
        ButtonManager.Game_buttons[1] = ButtonManager.replay_button
        #ButtonManager.Pause_menu_buttons[2] = ButtonManager.replay_button        
        
        
    def show_buttons(self):
        if in_menu:
            Active_buttons = ButtonManager.Menu_buttons
            pygame.mouse.set_visible(True)

            
        elif paused:
            Active_buttons = ButtonManager.Pause_menu_buttons
            pygame.draw.rect(screen, 'green', (round(WIDTH/2) - 60,
                             round(HEIGHT/2) - 315, 120, 60), border_radius=20)
        else:
            Active_buttons = ButtonManager.Game_buttons
            
        for button in Active_buttons:
            button.draw(screen)
            
    def check_click(self):
        if in_menu:
            Active_buttons = ButtonManager.Menu_buttons
            
        elif paused:
            Active_buttons = ButtonManager.Pause_menu_buttons
            pygame.draw.rect(screen, 'green', (round(WIDTH/2) - 60,
                             round(HEIGHT/2) - 15, 120, 60), border_radius=20)
        else:
            Active_buttons = ButtonManager.Game_buttons
        
        for button in Active_buttons:
            button.check_click(event)
        
    
ButMan = ButtonManager()

brick_wall = buttons.fetch_file('pictures', 'wall.png')
while not finished:
    counted_FPS = clock.get_fps()
    screen.blit(brick_wall, (0, 0))
    if in_menu:
        screen.blit(BACKGROUND, (0,0))

        # рисуем собранные факультеты
        faculties = ducks.get_faculties()
        i = 0
        while i < len(faculties):
            f = faculties[i]
            screen.blit(ducks.duck_image[f][2], (10 + 90*i, 10))
            i += 1
            
        
        
    
    if not in_menu:
        destr, destr_mask, r_vector, v = drip_seq(
            screen, destr, destr_x, destr_y, destr_mask,
            indestr,indestr_x, indestr_y, indestr_mask,
            r_vector, v,
            paused, shape = shape)

    ButMan.show_buttons()
    
    pygame.display.update()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ButMan.check_click()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                control_shape()
        
pygame.quit()
print(counted_FPS)
