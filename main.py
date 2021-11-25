import pygame
from pygame.draw import *
from buttons import *



WIDTH = 700
HEIGHT = 800
FPS = 30


pygame.display.set_icon(icon)
pygame.display.set_caption(('Проект Сивухин'))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


finished = False
paused = True

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

while not finished:
    screen.fill('white')
    ButMan.show_buttons()
    Cat.draw(screen)
    #Cat.angle += 0.1 кот распадается на атоме при таком кручении
    pygame.display.update()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ButMan.check_click()
        
pygame.quit()
