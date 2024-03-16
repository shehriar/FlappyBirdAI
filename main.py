import os
import neat
import pygame
from bird import Bird
from pipes import Pipes

pygame.init()

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 700

BACKGROUND = pygame.transform.scale(pygame.image.load("assets/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

firstPipeDrawn = False
secondPipeDrawn = False

firstPipes = Pipes("First")
secondPipes = Pipes("First")

font = pygame.font.Font('freesansbold.ttf', 32)
smallerFont = pygame.font.Font('freesansbold.ttf', 24)

gen = 0
highestScore = 0

def drawPipes(bird):
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


def incrementScore(bird):
    global firstPipes, secondPipes
    if bird.xPos == firstPipes.xPos + 50:
        return True
    if bird.xPos == secondPipes.xPos + 50:
        return True
    return False

def checkCollision(bird):
    global firstPipes, secondPipes
    if bird.xPos > firstPipes.xPos - 25 and bird.xPos < firstPipes.xPos + 25:
        if bird.yPos < firstPipes.height or bird.yPos > firstPipes.height + firstPipes.gap:
            return True, -1
    if bird.xPos > secondPipes.xPos - 25 and bird.xPos < secondPipes.xPos + 50:
        if bird.yPos < secondPipes.height or bird.yPos > secondPipes.height + secondPipes.gap:
            return True, -1
    if bird.yPos > 530 or bird.yPos < 10:
        return True, 0

    return False, 0

def reset_game():
    global firstPipeDrawn, secondPipeDrawn, firstPipes, secondPipes, score
    firstPipeDrawn = False
    secondPipeDrawn = False
    firstPipes = Pipes("First")
    secondPipes = Pipes("First")
    score = 0

def main(genomes, config):
    global gen, highestScore

    if gen == 0:
        gen = 1

    score = 0

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird())
        g.fitness = 0
        ge.append(g)

    running = True
    gameLost = False
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


        screen.blit(BACKGROUND, (0, 0))
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            gen+=1
            reset_game()
            break

        whichPipeNext = firstPipes
        if len(birds) > 0:
            if firstPipes.xPos + 25 < birds[0].xPos < secondPipes.xPos:
                whichPipeNext = secondPipes
            if secondPipes.xPos + 25 < birds[0].xPos < firstPipes.xPos:
                whichPipeNext = firstPipes

        for x, bird in enumerate(birds):
            bird.birdFalling()
            ge[x].fitness += 0.1

            # output = nets[x].activate((bird.yPos, abs(bird.yPos - whichPipeNext.height), abs(bird.yPos - (577 - whichPipeNext.yPos - whichPipeNext.height - whichPipeNext.gap))))
            output = nets[x].activate((
                bird.yPos,  # Bird's current vertical position
                abs(bird.yPos - whichPipeNext.height),  # Distance to the top of the gap
                abs(bird.yPos - (whichPipeNext.height + whichPipeNext.gap)),
                whichPipeNext.xPos,
            ))

            # print(output)
            if output[0] > 0.5:
                bird.isFlying = True
                bird.setInitYPos(bird.yPos)

            if bird.isFlying:
                bird.birdFlying()
            else:
                bird.birdFalling()

        for x, bird in enumerate(birds):
            bird.draw(screen)
            if incrementScore(bird):
                score += 1
                for g in ge:
                    if score > highestScore:
                        highestScore = score
                        g.fitness += 8
                    g.fitness += 8

            drawPipes(birds[0])
            collision, fitness = checkCollision(bird)
            if collision:
                ge[x].fitness -= 2
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        text = font.render(str(score), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        gen_label = smallerFont.render("Generation: " + str(gen - 1), 1, (255, 255, 255))
        screen.blit(gen_label, (10, 10))

        alive_label = smallerFont.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
        screen.blit(alive_label, (10, 50))

        highest_label = smallerFont.render("Highest: " + str(highestScore), 1, (255, 255, 255))
        screen.blit(highest_label, (250, 10))

        screen.blit(text, textRect)

        if not birds:
            gen += 1
            reset_game()
            running = False
            break

        pygame.display.update()
        clock.tick(40)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(main, 20)

    print("Best genome", winner)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.neat.txt")
    run(config_path)
