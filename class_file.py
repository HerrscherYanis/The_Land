#import asyncio
import pygame
import json

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
import db

class Screen:
    object_stock = []
    def __init__(self,SCREEN_WIDTH, SCREEN_HEIGHT, name = "The Land"):
        db.init()
        self.size = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.name = name
        self.map = 'data/map/map.json'
        pygame.init()
        pygame.display.set_caption(self.name)
        self.run = True
        self.clock = pygame.time.Clock()
        self.inventory = ["Potion", "Épée"]
        self.spawned_items = [] 


        self.movement = [False, False]

        self.assets = {
        'decor': load_images('tiles/decor'),
        'grass': load_images('tiles/grass'),
        'large_decor': load_images('tiles/large_decor'),
        'stone': load_images('tiles/stone'),
        'player': load_image('entities/player/idle/00.png'),
        'background': load_image('background.png'),
        'clouds': load_images('clouds'),
        'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
        'player/run': Animation(load_images('entities/player/run'), img_dur=4),
        'player/jump': Animation(load_images('entities/player/jump')),
        'player/slide': Animation(load_images('entities/player/slide')),
        'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
    }
                    
        self.clouds = Clouds(self.assets['clouds'], count=16)
        
        self.player = Player(self, (50, 90), (8, 15))

        self.enemy = Enemy(150, 150) # position de départ de l'ennemi 
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load(self.map)
        
        self.scroll = [0, 0]

    def start(self):
        while self.run: 
            if self.player.check("d") == True:
                self.display.fill((14,219,248))
                
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                
                self.clouds.update()
                self.clouds.render(self.display, offset=render_scroll)
                
                self.tilemap.render(self.display, offset=render_scroll)
                
                self.player.jump(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

                self.enemy.update(self.player.rect().center)
                self.enemy.render(self.display, offset=render_scroll)

                for item in self.spawned_items:
                    color = (255, 255, 0) if item["type"] == "potion" else (100, 100, 255)
                    pygame.draw.rect(self.display, color, pygame.Rect(
                        item["pos"][0] - render_scroll[0],
                        item["pos"][1] - render_scroll[1],
                        10, 10))

                player_rect = pygame.Rect(self.player.pos[0], self.player.pos[1], 10, 10)
                to_remove = []
                for item in self.spawned_items:
                    item_rect = pygame.Rect(item["pos"][0], item["pos"][1], 10, 10)
                    if player_rect.colliderect(item_rect):
                        print(f"{item['type'].capitalize()} ramassée !")
                        to_remove.append(item)
                        # Tu peux ici ajouter des effets (ex : soin, épée équipée...)

                for item in to_remove:
                    self.spawned_items.remove(item)


                self.draw_inventory(self.display)

                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.player.fight(self.tilemap, (self.movement[1] - self.movement[0], 0))
                        if event.key == pygame.K_s:
                            self.save()
                        if event.key == pygame.K_l:
                            self.load()
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = True
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = True
                        if event.key == pygame.K_UP:
                            if self.player.retry_jump == True:
                                self.player.velocity[1] = -3
                                self.player.retry_jump = False
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = False
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        scale_x = self.size.get_width() / self.display.get_width()
                        scale_y = self.size.get_height() / self.display.get_height()
                        scaled_mouse = (mouse_pos[0] / scale_x, mouse_pos[1] / scale_y)

                        for rect, item in self.item_rects:
                            if rect.collidepoint(scaled_mouse):
                                if item == "Potion":
                                    self.spawned_items.append({"type": "potion", "pos": [self.player.pos[0] + 30, self.player.pos[1]]})
                                elif item == "Épée":
                                    self.spawned_items.append({"type": "epee", "pos": [self.player.pos[0] + 30, self.player.pos[1]]})

                
                self.size.blit(pygame.transform.scale(self.display, self.size.get_size()), (0, 0))
                pygame.display.update()
                self.clock.tick(60)

    def save(self):
        with open("data/save.json", "w", encoding='UTF-8') as file:
            file.write('{"screen" : {"map" : "' + self.map + '"},"player" :{ "pos" : [' + str(self.player.pos[0]) + "," + str(self.player.pos[1]) + ']} }')
            print("save")
    def load(self):
        with open("data/save.json", "r", encoding='UTF-8') as file:
            data = json.loads(file.read())
            print("load")
            self.tilemap.load(data["screen"]["map"])
            self.player.pos = data["player"]["pos"]
    def draw_inventory(self, screen):
        font = pygame.font.SysFont(None, 24)
        self.item_rects = []  # Stocker les zones cliquables

        for i, item in enumerate(self.inventory):
            text = font.render(item, True, (255, 255, 255))
            rect = text.get_rect(topleft=(10, 10 + i * 20))
            screen.blit(text, rect)
            self.item_rects.append((rect, item))  # Sauvegarde pour le clic

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 0, 0))  # Couleur rouge pour l’ennemi
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player_pos):
        if self.rect.x < player_pos[0]: self.rect.x += 1
        if self.rect.x > player_pos[0]: self.rect.x -= 1
        if self.rect.y < player_pos[1]: self.rect.y += 1
        if self.rect.y > player_pos[1]: self.rect.y -= 1

    def render(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
