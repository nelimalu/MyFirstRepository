'''
Computer Training Pong by Luka Jovanovic
'''

import pygame
import random
import math
import time
import neat
import os
import pickle
pygame.font.init()

WIN_WIDTH = 700
WIN_HEIGHT = 600

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Pong!")

MAIN_FONT = pygame.font.SysFont('comicsans', 30)
FINAL_FONT = pygame.font.SysFont('comicsans', 43)
STAT_FONT = pygame.font.SysFont('comicsans', 50)
SCORE_FONT = pygame.font.SysFont('comicsans', 160)

gen = 0
start = time.time()

class Board:
    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.vel = 3.5

    def move(self, direction):
        if direction == 'up' and self.y >= 0:
            self.y -= self.vel
        elif direction == 'down' and self.y <= 460:
            self.y += self.vel

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 10, 140))

class Ball:
    def __init__(self):
        self.x = 346
        self.y = 300
        self.vel = 2
        self.tilt = random.randrange(45,135)
        self.direction = random.randint(1,2)

    def draw(self, win):
        try:
            pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 10, 10))
        except: pass

    def bounce(self):
        self.tilt = (180 - self.tilt) % 360
        self.vel *= 1.1

    def vertical_bounce(self):
        self.tilt = (360 - self.tilt) % 360
        self.vel *= 1.1

    def first_move(self):
        self.tilt = random.randrange(45,135)
        self.direction = random.randint(1, 2)
        if self.direction == 1:
            tilt_radians = math.radians(self.tilt)
            self.x += self.vel * math.sin(tilt_radians)
            self.y -= self.vel * math.cos(tilt_radians)
        if self.direction == 2:
            self.tilt = self.tilt + 180
            tilt_radians = math.radians(self.tilt)
            self.x += self.vel * math.sin(tilt_radians)
            self.y -= self.vel * math.cos(tilt_radians)

    def move(self):
        tilt_radians = math.radians(self.tilt)
        self.x += self.vel * math.sin(tilt_radians)
        self.y -= self.vel * math.cos(tilt_radians)

    def reset(self):
        self.tilt = random.randrange(45, 135)
        self.direction = random.randint(1, 2)
        self.x = 346
        self.y = 300
        self.vel = 2


def draw_game(win, player1_board, ball, player2_board, player1_score, player2_score, total_time):
    win.fill([32, 32, 32])

    text = MAIN_FONT.render('PONG', 1, (128, 128, 128))
    win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 8))

    text = SCORE_FONT.render(str(player1_score), 1, (128, 128, 128))
    win.blit(text, (WIN_WIDTH / 4 - text.get_width() / 2, 300 - text.get_height() / 2))

    text = SCORE_FONT.render(str(player2_score), 1, (128, 128, 128))
    win.blit(text, ((WIN_WIDTH / 4) * 3 - text.get_width() / 2, 300 - text.get_height() / 2))

    text = MAIN_FONT.render('Generation: ' + str(gen), 1, (200, 200, 200))
    win.blit(text, (20, 10))

    text = MAIN_FONT.render('Time Elapsed: ' + str(total_time), 1, (200, 200, 200))
    win.blit(text, (20, 30))

    pygame.draw.rect(win, (64, 64, 64), (350, 30, 2, 700))

    player1_board.draw(win)
    player2_board.draw(win)
    ball.draw(win)


def eval_genomes(genomes, config):

    global WIN, gen
    gen += 1

    nets = []
    boards = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config) # create a network for each bird
        nets.append(net)

        '''
        with open('best.pickle', 'rb') as pickle_file:
            x = pickle.load(pickle_file)
        nets.append(x)
        '''

        ge.append(genome) #add the genome to genomes list

    boards.append(Board(680, 230))
    boards.append(Board(10, 230))

    cmpt1_score = 0
    cmpt2_score = 0
    ball = Ball()
    justonce = True
    run = True

    clock = pygame.time.Clock()

    while run and len(boards) > 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        for x, board in enumerate(boards):  # give each bird a fitness of 0.1 for each frame it stays alive
            #ge[x].fitness += 0.01

            output = nets[boards.index(board)].activate((board.y + 10, board.y - ball.y, board.x - ball.x, ball.vel))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump (should the bird jump? yes or no)
                board.move('up')
                #ge[x].fitness += 0.2
            elif output[0] <= -0.5:
                board.move('down')
                #ge[x].fitness += 0.2

        if justonce:
            justonce = False

        ball.move()
        if ball.y <= 0 or ball.y >= 590:
            ball.bounce()

        if ball.x <= 0:
            cmpt2_score += 1
            ge[1].fitness += 2
            justonce = True
            ball.reset()

        if ball.x >= 690:
            cmpt1_score += 1
            ge[0].fitness += 2
            justonce = True
            ball.reset()

        if boards[1].x + 10 >= int(ball.x):
            for i in range(int(boards[1].y), int(boards[1].y + 140)):
                if int(ball.y) == i:
                    ball.vertical_bounce()
                    ge[0].fitness += 2

        if boards[0].x <= int(ball.x) + 10:
            for i in range(int(boards[0].y), int(boards[0].y + 140)):
                if int(ball.y) == i:
                    ball.x = boards[0].x - 11
                    ball.vertical_bounce()
                    ge[1].fitness += 2


        end = time.time()
        total_time = end - start
        total_mins = int(total_time / 60)
        total_seconds = int(total_time % 60)
        total_hours = int(total_mins / 60)
        final_time = str(total_hours) + ':' + str(total_mins) + ':' + str(total_seconds)

        draw_game(WIN, boards[0], ball, boards[1], cmpt1_score, cmpt2_score, final_time)
        pygame.display.flip()

        if cmpt1_score == 7:
            pickle.dump(nets[1], open("best.pickle", "wb"))
            ge[1].fitness -= 10
            ge[0].fitness += 5
            for board in boards:
                nets.pop(boards.index(board))
                ge.pop(boards.index(board))
                boards.pop(boards.index(board))

        elif cmpt2_score == 7:
            pickle.dump(nets[0], open("best.pickle", "wb"))
            ge[0].fitness -= 10
            ge[1].fitness += 5
            for board in boards:
                nets.pop(boards.index(board))
                ge.pop(boards.index(board))
                boards.pop(boards.index(board))

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 500)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
