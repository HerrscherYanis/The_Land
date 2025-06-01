import class_file as cf
import db

import pygame
import class_file as cf

def main_menu(screen):
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    text = font.render("Appuyez sur ESPACE pour commencer", True, (255, 255, 255))
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, (50, 150))  # Position à ajuster si besoin
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Taille provisoire
    main_menu(screen)

    jeu = cf.Screen(800, 600)
    jeu.start()


screen = cf.Screen(640,480)
db.player_gen("df", 1, 21, 1, 0)
screen.start()