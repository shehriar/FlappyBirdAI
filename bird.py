import pygame
JUMP_HEIGHT = 20
Y_GRAVITY = 1

class Bird:
    def __init__(self):
        self.height = 40
        self.width = 40
        self.color = (255, 255, 0)
        self.xPos = 150
        self.yPos = 200
        self.isFlying = False
        self.initYPos = self.yPos

    def draw(self, screen):
        if self.isFlying:
            img = pygame.image.load("assets/bird-flying.png")
        else:
            img = pygame.image.load("assets/bird-falling.png")

        birdPosition = (self.xPos, self.yPos)
        img = pygame.transform.scale(img, (self.width, self.height))

        screen.blit(img, birdPosition)
        # pygame.draw.rect(screen, self.color, pygame.Rect(self.xPos, self.yPos, self.width, self.height))

    def birdFalling(self):
        FALLING_SPEED = 4
        if self.yPos < 540:
            self.yPos += FALLING_SPEED

    def setInitYPos(self, yPos):
        self.initYPos = yPos

    def birdFlying(self):
        if self.isFlying:
            self.yPos -= 7
            if self.yPos < self.initYPos - 60:
                self.isFlying = False