import os
import pygame
from scripts.menu import Menu

def start():
    os.environ['SDL_VIDEO_CENTERED'] = '1' 
    pygame.init()

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_w, screen_h))

    caption = "Sokoban Game"
    pygame.display.set_caption(caption)
    
    icon = pygame.image.load(r"gameSokoban\assets\images\icon.png").convert_alpha()
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)

    menu = Menu(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or not menu.handle_events(event):
                running = False

        if running:    
            menu.run()

    menu.release()
    pygame.quit()