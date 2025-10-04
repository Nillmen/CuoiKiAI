import pygame
from scripts.menu import Menu
from scripts.gameplay import Gameplay
from scripts.window import Window

pygame.init()

def start():
    
    window = Window()

    menu = Menu(window)
    game_play = Gameplay(window)

    screens = {
        "menu" : menu,
        "game_play" : game_play
    }

    running = True
    while running:
        screen = screens[window.get_data("status_screen")]
        
        running = screen.handle_events(None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or not screen.handle_events(event):
                running = False

        if running:    
            screen.run()

    screen.release()
    pygame.quit()