#import asyncio
import pygame
import time
import function_file as func

class Screen:
    object_stock = {}
    def __init__(self,SCREEN_WIDTH, SCREEN_HEIGHT, name = "The Land"):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.name = name

    def start(self):
            pygame.display.set_caption(self.name)
            self.run = True
            self.clock = pygame.time.Clock()
            self.update()

    def update(self):
        while self.run: 
            pygame.display.update()

            # self.screen.fill((0, 0, 0))
            for im in self.image_stock:
                try:
                    self.screen.blit(im[0], im[1])
                except:
                    pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.clock.tick(60)
        pygame.quit()

    def load(self):
        screen.blit(image.img,(image.width,image.height))

    def get(self, name, object_class):
        self.object_stock.append({ name : object_class })
    #    self.image_stock.update({image.name : image})


class Image:
    def __init__(self, path, width, height):
        self.name = path.split("/")[-1]
        self.size = (width, height)
        try:
            self.img = pygame.image.load(path)
        except:
            print("Error, path not found!")
            self.img = pygame.image.load('./resources/Error.jpg')



class Object:
    def __init__(self,Image,x, y):
        self.Image = Image
        self.coord = (x , y)


class Player(Object):
    def __init__(self):
        super().__init__(Image,x, y)
        self.life = 0

class Ennemy(Object):
    super().__init__(Image,x, y)
    def __init__(self):
        pass

