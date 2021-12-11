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


finished = False
paused = True
in_menu = True
loaded_level = 1

def quit():
    global finished
    finished = True

def go_to_menu():
    global in_menu
    in_menu = True

def playpause():
    global paused
    if not paused:
        paused = True
    else:
        paused = False

def load_level(level):
    
    global destr, destr_x, destr_y, destr_mask, \
    indestr, indestr_x, indestr_y, indestr_mask, \
    r_vector, v,\
    in_menu, loaded_level

    in_menu = False
    loaded_level = level
    
    
    destr, destr_x, destr_y, destr_mask = levels[level-1]['destr']()

    indestr, indestr_x, indestr_y, indestr_mask = levels[level-1]['indestr']()
    
    r_vector, v = model.make_water(400, 600, -200, 0, 200) # делаем массив воды

    Duck.duck_array = levels[level-1]['ducks']()
    
    Droplet.water_array = [] # уничтожили все капли


class ButtonManager():

    global paused, WIDTH, HEIGHT, in_menu
    
    play_button =  Button(WIDTH / 2, HEIGHT /  2, button_play_surf, playpause)
    pause_button =  Button(WIDTH - 30, 30 , button_pause_surf, playpause)
    quit_button = Button(WIDTH / 2, HEIGHT /  2 + 30, button_quit_surf,
                         go_to_menu)
    replay_button = Button(40, 40, button_replay_surf, load_level,
                           argument=loaded_level)
    level_buttons = []
    for i in range(len(level_button_surf)):
        level_buttons.append(Button(WIDTH / 2 - 120 + 120 * i, HEIGHT /  2,
                              level_button_surf[i],
                              load_level, argument = i + 1))
    
    Pause_menu_buttons = [quit_button, play_button, replay_button]
    Game_buttons = [pause_button, replay_button]
    Menu_buttons = level_buttons
    
    def show_buttons(self):
        if in_menu:
            Active_buttons = ButtonManager.Menu_buttons
            
        elif paused:
            Active_buttons = ButtonManager.Pause_menu_buttons
            pygame.draw.rect(screen, 'green', (round(WIDTH/2) - 60,
                             round(HEIGHT/2) - 15, 120, 60), border_radius=20)
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

cunted_FPS = 0
while not finished:
    counted_FPS = clock.get_fps()
    screen.fill('red')
    if in_menu:
        screen.blit(BACKGROUND, (0,0))
    
    
    if not in_menu:
        destr, destr_mask, r_vector, v = drip_seq(
            screen, destr, destr_x, destr_y, destr_mask,
            indestr,indestr_x, indestr_y, indestr_mask,
            r_vector, v,
            paused)
    
    #screen.blit(level_screen, (0, 0))
    
    ButMan.show_buttons()
    
    pygame.display.update()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ButMan.check_click()
        
pygame.quit()
print(counted_FPS)
