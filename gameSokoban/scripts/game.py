import pygame
from scripts.menu import Menu
from scripts.window import Window

def start():
    
    window = Window()

    menu = Menu(window)

    running = True
    while running:
        running = menu.handle_events(None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or not menu.handle_events(event):
                running = False

        if running:    
            menu.run()

    menu.release()
    pygame.quit()