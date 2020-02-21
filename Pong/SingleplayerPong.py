'''
Singleplayer Pong by Luka Jovanovic
'''

import pygame
import random
import math
import pickle
pygame.font.init()

WIN_WIDTH = 700
WIN_HEIGHT = 600

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Pong!")

MAIN_FONT = pygame.font.Font('BebasNeue-Regular.ttf', 30)
FINAL_FONT = pygame.font.Font('BebasNeue-Regular.ttf', 43)
STAT_FONT = pygame.font.Font('BebasNeue-Regular.ttf', 50)
SCORE_FONT = pygame.font.Font('BebasNeue-Regular.ttf', 160)

class Board:
    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.vel = 0.5  # 0.5

    def move(self, direction):
        if direction == 'up' and self.y >= 0:
            self.y -= self.vel
        elif direction == 'down' and self.y <= 460:
            self.y += self.vel

    def draw(self, WIN):
        pygame.draw.rect(WIN, (255, 255, 255), (self.x, self.y, 10, 140))

class Ball:
    def __init__(self, difficulty):
        self.x = 346
        self.y = 300
        self.vel = 0.35  # 0.35
        self.radius = 6
        self.tilt = random.randrange(45,135)
        self.direction = random.randint(1,2)
        self.choices = [-45, 45]

    def draw(self, WIN):
        try:
            pygame.draw.rect(WIN, (255, 255, 255), (self.x, self.y, 10, 10))
        except: pass

    def bounce(self):
        self.tilt = (180 - self.tilt) % 360
        self.vel *= 1.02  # 1.02

    def vertical_bounce(self):
        self.tilt = (360 - self.tilt) % 360
        self.vel *= 1.02  # 1.02

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
        self.vel = 0.35 # 0.35


def draw_game(WIN, player1_board, ball, player2_board, player1_score, player2_score):
    WIN.fill([32, 32, 32])

    text = MAIN_FONT.render('PONG', 1, (128, 128, 128))
    WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 8))

    text = SCORE_FONT.render(str(player1_score), 1, (128, 128, 128))
    WIN.blit(text, (WIN_WIDTH / 4 - text.get_width() / 2, 300 - text.get_height() / 2))

    text = SCORE_FONT.render(str(player2_score), 1, (128, 128, 128))
    WIN.blit(text, ((WIN_WIDTH / 4) * 3 - text.get_width() / 2, 300 - text.get_height() / 2))

    pygame.draw.rect(WIN, (64, 64, 64), (350, 45, 2, 700))

    player1_board.draw(WIN)
    player2_board.draw(WIN)
    ball.draw(WIN)


def main():

    global WIN

    nets = []

    with open('TheAI.pickle', 'rb') as pickle_file:
        x = pickle.load(pickle_file)
    nets.append(x)

    computer = Board(670, 230)
    player = Board(20, 230)

    score2 = 0
    score1 = 0
    ball = Ball(1)
    justonce = True
    end = False
    begin = False
    playUntil = 7
    playAgain = True
    run = True

    while playAgain:
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    playAgain = False

            while begin == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        begin = True
                        run = False
                        playAgain = False

                draw_game(WIN, player, ball, computer, score1, score2)

                pygame.draw.rect(WIN, (255, 255, 255), (350 - 103, 300 - 103, 206, 206))
                pygame.draw.rect(WIN, (200, 200, 200), (250, 200, 200, 200))

                text = STAT_FONT.render('CLICK TO', 1, (32, 32, 32))
                WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 280 - text.get_height()/2))
                text = STAT_FONT.render('BEGIN', 1, (32, 32, 32))
                WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 320 - text.get_height() / 2))

                mousepos = pygame.mouse.get_pos()

                if mousepos[0] > 247 and mousepos[0] < 453 and mousepos[1] > 198 and mousepos[1] < 405:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            begin = True
                            run = True

                    pygame.draw.rect(WIN, (0, 0, 0), (350 - 103, 300 - 103, 206, 206))
                    pygame.draw.rect(WIN, (55, 55, 55), (250, 200, 200, 200))

                    text = STAT_FONT.render('CLICK TO', 1, (255, 255, 255))
                    WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 280 - text.get_height() / 2))
                    text = STAT_FONT.render('BEGIN', 1, (255, 255, 255))
                    WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 320 - text.get_height() / 2))
                else:
                    pygame.draw.rect(WIN, (255, 255, 255), (350 - 103, 300 - 103, 206, 206))
                    pygame.draw.rect(WIN, (200, 200, 200), (250, 200, 200, 200))

                    text = STAT_FONT.render('CLICK TO', 1, (32, 32, 32))
                    WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 280 - text.get_height() / 2))
                    text = STAT_FONT.render('BEGIN', 1, (32, 32, 32))
                    WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 320 - text.get_height() / 2))

                pygame.display.flip()

            output = nets[0].activate((computer.y - 5, computer.y - ball.y, computer.x - ball.x))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump (should the bird jump? yes or no)
                computer.move('up')
            elif output[0] <= -0.5:
                computer.move('down')

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] or keys[pygame.K_KP8] or keys[pygame.K_UP]:
                player.move('up')
            if keys[pygame.K_s] or keys[pygame.K_KP2] or keys[pygame.K_DOWN]:
                player.move('down')

            if justonce:
                ball.first_move()
                justonce = False

            ball.move()
            if ball.y <= 0 or ball.y >= 590:
                ball.bounce()

            if ball.x <= 0:
                score2 += 1
                justonce = True
                ball.reset()

            if ball.x >= 690:
                score1 += 1
                justonce = True
                ball.reset()

            try:
                if ball.vel <= 0.9:
                    if player.x + 10 == int(ball.x):
                        for i in range(int(player.y), int(player.y + 141)):
                            if int(ball.y) == i:
                                ball.vertical_bounce()

                    if computer.x == int(ball.x) + 10:
                        for i in range(int(computer.y), int(computer.y + 141)):
                            if int(ball.y) == i:
                                ball.vertical_bounce()
                else:
                    if player.x + 10 >= int(ball.x):
                        for i in range(int(player.y), int(player.y + 141)):
                            if int(ball.y) == i:
                                ball.vertical_bounce()

                    if computer.x <= int(ball.x) + 10:
                        for i in range(int(computer.y), int(computer.y + 141)):
                            if int(ball.y) == i:
                                ball.vertical_bounce()

                draw_game(WIN, player, ball, computer, score1, score2)
                pygame.display.flip()
            except:
                pass

            if score1 == playUntil or score2 == playUntil:
                end = True
                run = False

        while end == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = False
                    playAgain = False

            draw_game(WIN, player, ball, computer, score1, score2)

            mousepos = pygame.mouse.get_pos()

            if mousepos[0] > 247 and mousepos[0] < 453 and mousepos[1] > 198 and mousepos[1] < 405:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        end = False

                pygame.draw.rect(WIN, (0, 0, 0), (350 - 103, 300 - 103, 206, 206))
                pygame.draw.rect(WIN, (55, 55, 55), (250, 200, 200, 200))

                text = FINAL_FONT.render('GAME OVER', 1, (255, 255, 255))
                WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 280 - text.get_height() / 2))
                text = MAIN_FONT.render('Click to play again', 1, (255, 255, 255))
                WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 320 - text.get_height() / 2))

            else:
                pygame.draw.rect(WIN, (255, 255, 255), (350 - 103, 300 - 103, 206, 206))
                pygame.draw.rect(WIN, (200, 200, 200), (250, 200, 200, 200))

                text = FINAL_FONT.render('GAME OVER', 1, (32, 32, 32))
                WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 280 - text.get_height() / 2))
                text = MAIN_FONT.render('Click to play again', 1, (32, 32, 32))
                WIN.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 320 - text.get_height() / 2))

            pygame.display.flip()

main()

pygame.quit()
quit()

