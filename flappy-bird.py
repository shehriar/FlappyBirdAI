import pygame
from bird import Bird
from pipes import Pipes

pygame.init()

SCREEN_WIDTH = 350
SCREEN_HEIGHT = 700

running = True

BACKGROUND = pygame.transform.scale(pygame.image.load("assets/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

bird = Bird()

firstPipeDrawn = False
secondPipeDrawn = False

firstPipes = Pipes("First")
secondPipes = Pipes("Second")

score = 0

font = pygame.font.Font('freesansbold.ttf', 32)

gameLost = False;

def drawPipes():
    global firstPipeDrawn, secondPipeDrawn, firstPipes, secondPipes
    if not firstPipeDrawn:
        firstPipes = Pipes("First")
        firstPipeDrawn = True

    if not secondPipeDrawn:
        if bird.xPos > firstPipes.xPos - 50:
            secondPipes = Pipes("Second")
            secondPipeDrawn = True

    if firstPipes.xPos < -50:
        firstPipeDrawn = False

    if secondPipes.xPos < -50:
        secondPipeDrawn = False

    if firstPipeDrawn:
        firstPipes.drawPipes(screen)
        firstPipes.moving()

    if secondPipeDrawn:
        secondPipes.drawPipes(screen)
        secondPipes.moving()
    return

def incrementScore():
    global firstPipes, secondPipes, bird, score
    if bird.xPos == firstPipes.xPos + 50:
        score += 1
    if bird.xPos == secondPipes.xPos + 50:
        score += 1

def checkCollision():
    global bird, firstPipes, secondPipes
    if bird.xPos > firstPipes.xPos - 25 and bird.xPos < firstPipes.xPos + 25:
        if bird.yPos < firstPipes.height or bird.yPos > firstPipes.height + firstPipes.gap:
            return True
    if bird.xPos > secondPipes.xPos - 25 and bird.xPos < secondPipes.xPos + 50:
        if bird.yPos < secondPipes.height or bird.yPos > secondPipes.height + secondPipes.gap:
            return True
    if bird.yPos > 530 or bird.yPos < 20:
        return True

    return False

while(running):
    screen.blit(BACKGROUND, (0,0))
    key = pygame.key.get_pressed()
    incrementScore()

    bird.draw(screen)
    drawPipes()

    text = font.render(str(score), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

    screen.blit(text, textRect)

    gameLost = checkCollision()
    if gameLost:
        running = False

    if key[pygame.K_SPACE]:
        bird.isFlying = True
        bird.setInitYPos(bird.yPos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if bird.isFlying:
        bird.birdFlying()
    else:
        bird.birdFalling()

    pygame.display.update()
    clock.tick(60)

pygame.quit()

if __name__ == '__main__':
    pass