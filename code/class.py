import pygame
import time

class screen:
    name = "The Land"
    SCREEN_WIDTH
    SCREEN_HEIGHT
    def __init__(self,SCREEN_WIDTH, SCREEN_HEIGHT, name = self.name):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
    
    def Run(self):
        pygame.display.set_caption(self.name)
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        run = True
        clock = pygame.time.Clock()

        while run:
            screen.fill((0, 0, 0))
   
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            clock.tick(60)
        pygame.quit()