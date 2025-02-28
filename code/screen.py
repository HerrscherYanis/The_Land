import pygame
import time

def screen(SCREEN_WIDTH, SCREEN_HEIGHT):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    run = True
    clock = pygame.time.Clock()

    while run:
        screen.fill((0, 0, 0))
   
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clock.tick(5)
    pygame.quit()

screen(500,500)