import pygame
from scripts.menu import Menu
from scripts.gameplay import Gameplay
from scripts.window import Window

pygame.init()

def start():
    
    window = Window()

    screen = None

    running = True
    while running:
        name = window.get_data("status_screen")
        if name == "menu" and not isinstance(screen, Menu):
            screen = Menu(window)

        elif name == "gameplay" and not isinstance(screen, Gameplay):
            screen = Gameplay(window)

        running = screen.handle_events(None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or not screen.handle_events(event):
                running = False

        if running:    
            screen.run()
        else:
            screen.release()

    pygame.quit()