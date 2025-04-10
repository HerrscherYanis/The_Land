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
                
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
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
