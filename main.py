import pygame
from pygame.draw import *
from buttons import *
import drip
import model
from drip import drip_seq, get_obstacles
import ducks
from ducks import *

WIDTH = 700
HEIGHT = 800
FPS = 30


pygame.display.set_icon(icon)
pygame.display.set_caption(('Проект Сивухин'))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


finished = False
paused = False

def quit():
    global finished
    finished = True

def pause():
    global paused
    paused = True

def play():
    global paused
    paused = False


class ButtonManager():

    global paused, WIDTH, HEIGHT
    
    play_button =  Button(WIDTH / 2, HEIGHT /  2, button_play_surf, play)
    pause_button =  Button(WIDTH - 30, 30 , button_pause_surf, pause)
    quit_button = Button(WIDTH / 2, HEIGHT /  2 + 30, button_quit_surf, quit)
    
    Menu_buttons = [quit_button, play_button]
    Game_buttons = [pause_button]
    
    def show_buttons(self):
        global paused
        if paused:
            Active_buttons = ButtonManager.Menu_buttons
            pygame.draw.rect(screen, 'green', (round(WIDTH/2) - 60,
                             round(HEIGHT/2) - 15, 120, 60), border_radius=20)
        else:
            Active_buttons = ButtonManager.Game_buttons
        for button in Active_buttons:
            button.draw(screen)
            
    def check_click(self):
        global paused
        if paused:
            Active_buttons = ButtonManager.Menu_buttons
            
        else:
            Active_buttons = ButtonManager.Game_buttons
        
        for button in Active_buttons:
            button.check_click(event)
        
    
ButMan = ButtonManager()

destr, destr_x, destr_y, destr_mask = get_obstacles(
        fetch_file('pictures', 'TEST.png','TEST'), 340, 240)
    
indestr, indestr_x, indestr_y, indestr_mask = get_obstacles(
    fetch_file('pictures', 'TEST1.png','TEST'), 340, 440)

r_vector, v = model.make_water(400, 600, -200, 0, 200) # делаем массив воды

Duck.duck_array.append(Duck(ducks.circle_function(200, 200, 10), 30, 200, 200,
                           using_mask = True)) # сделали утку

while not finished:
    screen.fill('red')
    
    #Cat.draw(screen) # очень ресурсозатратно 
    #Cat.angle += 2
    
    destr, destr_mask, r_vector, v = drip_seq(
        screen, destr, destr_x, destr_y, destr_mask,
        indestr,indestr_x, indestr_y, indestr_mask,
        r_vector, v,
        paused)
    
    ButMan.show_buttons()
    
    pygame.display.update()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ButMan.check_click()
        
pygame.quit()
