import pygame
import time
import function_file as func

class screen:
    image_stock = {}
    def __init__(self,SCREEN_WIDTH, SCREEN_HEIGHT, name = "The Land"):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.name = name

    def run(self):
        pygame.display.set_caption(self.name)
        self.run = True
        self.clock = pygame.time.Clock()
        while self.run:
            
            self.screen.fill((0, 0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.clock.tick(60)
        pygame.quit()

        def start(self):
            pass
        def update(self):
            pass

    def load(self):
        screen.blit(image.img,(image.width,image.height))

    def get(self, image):
        self.image_stock.update({image.name : image})
        print(self.image_stock.keys()[0].name)


class image:
    def __init__(self, path, width, height):
        self.name = path.split("/")[-1]
        self.width = width
        self.height = height
        try:
            self.img = pygame.image.load(image)
        except:
            print("Error, path not found!")
            self.img = pygame.image.load('./resources/Error.jpg')