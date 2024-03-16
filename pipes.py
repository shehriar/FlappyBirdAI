import random
import pygame

class Pipes:
    def __init__(self, name):
        self.name = name
        self.height = random.randint(110, 240)
        self.width = 50
        self.gap = 170
        self.spaceBetweenPipes = 300
        self.color = (0, 255, 0)
        self.xPos = 500
        self.yPos = 0


    def drawPipes(self, screen):
        topImg = pygame.image.load('assets/top-pipe.png')
        bottomImg = pygame.image.load('assets/bottom-pipe.png')

        topPipePosition = (self.xPos, self.yPos)
        bottomPipePosition = (self.xPos, self.yPos + self.height + self.gap)

        topImg = pygame.transform.scale(topImg, (self.width, self.height))
        bottomImg = pygame.transform.scale(bottomImg, (self.width, 577 - self.yPos - self.height - self.gap))

        screen.blit(topImg, topPipePosition)
        screen.blit(bottomImg, bottomPipePosition)

    def moving(self):
        self.xPos -= 2