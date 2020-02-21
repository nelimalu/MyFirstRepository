'''
Two Player Pong by Luka Jovanovic
'''

import pygame
import random
import math
# these three imports are required. Use 'pip install pygame'
# in your command prompt to use the pygame module.

pygame.font.init()

playUntil = 7
# adjust this value to decide how many points are required to win.

WIN_WIDTH = 700
WIN_HEIGHT = 600
# these values decide the size of the screen.

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # define the screen.
pygame.display.set_caption("Pong!") # set the title.

MAIN_FONT = pygame.font.SysFont('comicsans', 30)
FINAL_FONT = pygame.font.SysFont('comicsans', 43)
STAT_FONT = pygame.font.SysFont('comicsans', 50)
SCORE_FONT = pygame.font.SysFont('comicsans', 160)
# define some fonts and font sizes.

# this class creates a board.
class Board:
    def __init__(self, x, y):
        self.y = y
        self.x = x  # x and y are starting locations.
        self.vel = 3.5  # this value decides how many pixels the board moves per frame.

    def move(self, direction):
        if direction == 'up' and self.y >= 0:
            self.y -= self.vel
        elif direction == 'down' and self.y <= 460:
            self.y += self.vel
        # define what up and down mean.

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 10, 140))
        # draw the board on the screen.

class Ball:
    def __init__(self):
        self.x = 346
        self.y = 300  # x and y are starting positions.
        self.vel = 2  # how many pixels it moves per frame.
        self.tilt = random.randrange(45,135)  # define a random angle the ball will begin moving in
        self.direction = random.randint(1,2)  # which side will it move towards.

    def draw(self, win):
        try:
            pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 10, 10)) # draw the ball.
        except:
            pass

    def bounce(self):
        self.tilt = (180 - self.tilt) % 360  # change the tilt if it hits a wall.
        self.vel *= 1.1  # speed up the ball.

    def vertical_bounce(self):
        self.tilt = (360 - self.tilt) % 360 # change the tilt if it hits a board.
        self.vel *= 1.1  # speed up the ball.

    def first_move(self):
        self.tilt = random.randrange(45,135)
        if self.direction == 1:
            tilt_radians = math.radians(self.tilt)
            self.x += self.vel * math.sin(tilt_radians)
            self.y -= self.vel * math.cos(tilt_radians)
        if self.direction == 2:
            self.tilt = self.tilt + 180
            tilt_radians = math.radians(self.tilt)
            self.x += self.vel * math.sin(tilt_radians)
            self.y -= self.vel * math.cos(tilt_radians)

        # this function decides at which angle the ball should begin,
        # and make the ball move in that direction.
        # this is only called after a person has scored, or at the start of the game.

    def move(self):
        tilt_radians = math.radians(self.tilt)  # make the tilt a radian.
        self.x += self.vel * math.sin(tilt_radians)  # move the ball according to the tilt.
        self.y -= self.vel * math.cos(tilt_radians)

    def reset(self):
        self.x = 346
        self.y = 300
        self.vel = 2
        # this function resets all stats to the beginning.
        # this is called after a player has scored.


def draw_game(win, player1_board, ball, player2_board, player1_score, player2_score):
    win.fill([32, 32, 32])  # make the background gray.

    text = MAIN_FONT.render('PONG', 1, (128, 128, 128))
    win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 8))
    # draw the word "PONG" at the top of the screen.

    text = SCORE_FONT.render(str(player1_score), 1, (128, 128, 128))
    win.blit(text, (WIN_WIDTH / 4 - text.get_width() / 2, 300 - text.get_height() / 2))
    # draw player 1's score.

    text = SCORE_FONT.render(str(player2_score), 1, (128, 128, 128))
    win.blit(text, ((WIN_WIDTH / 4) * 3 - text.get_width() / 2, 300 - text.get_height() / 2))
    # draw player 2's score.

    pygame.draw.rect(win, (64, 64, 64), (350, 30, 2, 700))
    # draw the line down the middle.

    player1_board.draw(win)  # draw the boards.
    player2_board.draw(win)
    ball.draw(win)  # draw the ball.


# this is the actual game
def main(win, playUntil):
    playAgain = True
    while playAgain:
        player1_board = Board(10, 230)
        player2_board = Board(680, 230)
        player1_score = 0
        player2_score = 0
        ball = Ball()
        # define some of the game features.

        begin = False
        justonce = True
        end = False
        run = False
        # boolean variables used to maintain separate parts of the game from overlap.

        clock = pygame.time.Clock()
        # make an frames per second timer

        # "begin" is the first screen that asks you to begin.
        while not begin:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if you click on the X button, quit the game.
                    begin = True
                    playAgain = False

            draw_game(win, player1_board, ball, player2_board, player1_score, player2_score)
            # draw the background.

            pygame.draw.rect(win, (255, 255, 255), (350 - 103, 300 - 103, 206, 206))
            pygame.draw.rect(win, (200, 200, 200), (250, 200, 200, 200))
            # draw the box that the words are in.

            text = STAT_FONT.render('CLICK TO', 1, (32, 32, 32))
            win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 280 - text.get_height()/2))
            text = STAT_FONT.render('BEGIN', 1, (32, 32, 32))
            win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 320 - text.get_height() / 2))
            # draw the words

            mousepos = pygame.mouse.get_pos()  # get the mouse coordinates.

            if mousepos[0] > 247 and mousepos[0] < 453 and mousepos[1] > 198 and mousepos[1] < 405:  # detect if the mouse is hovering over the box
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        begin = True
                        run = True
                        # if the player clicks in the box, begin the game.

                pygame.draw.rect(win, (0, 0, 0), (350 - 103, 300 - 103, 206, 206))
                pygame.draw.rect(win, (55, 55, 55), (250, 200, 200, 200))

                text = STAT_FONT.render('CLICK TO', 1, (255, 255, 255))
                win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 280 - text.get_height() / 2))
                text = STAT_FONT.render('BEGIN', 1, (255, 255, 255))
                win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 320 - text.get_height() / 2))
                # draw the same text but inverted colours.

            pygame.display.flip()
            # update the screen.


        while run:
            clock.tick(60)  # define how many frames per second you would like.

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if you click on the X button, quit the game.
                    run = False
                    playAgain = False

            keys = pygame.key.get_pressed()  # detect all keys that are pressed.

            if keys[pygame.K_w]:
                player1_board.move('up')
            if keys[pygame.K_s]:
                player1_board.move('down')
            if keys[pygame.K_KP_PLUS] or keys[pygame.K_UP]:
                player2_board.move('up')
            if keys[pygame.K_KP_ENTER] or keys[pygame.K_DOWN]:
                player2_board.move('down')
            # move the boards up or down.

            if justonce:
                ball.first_move()
                justonce = False
                # if the game just began, call the first_move function.

            ball.move()  # move the ball
            if ball.y <= 0 or ball.y >= 590:
                ball.bounce()
                # if the ball hits the ceiling or floor, bounce.

            if ball.x <= 0:
                player2_score += 1
                justonce = True
                ball.reset()
                # if the ball gets past player 1's board, give player 2 a point and reset the game.

            if ball.x >= 690:
                player1_score += 1
                justonce = True
                ball.reset()
                # if the ball gets past player 2's board, give player 1 a point and reset the game.

            if player1_board.x + 10 >= int(ball.x):
                for i in range(int(player1_board.y), int(player1_board.y + 140)):
                    if int(ball.y) == i:
                        ball.vertical_bounce()
                        # detect if the ball hits the board and make it bounce.

            if player2_board.x <= int(ball.x) + 10:
                for i in range(int(player2_board.y), int(player2_board.y + 140)):
                    if int(ball.y) == i:
                        ball.x = player2_board.x - 11  # this is here to prevent a bug.
                        ball.vertical_bounce()
                        # detect if the ball hits the board and make it bounce.

            if player1_score == playUntil or player2_score == playUntil:
                end = True
                run = False
                # if anyone reaches the winning score, end the game and show the "end" screen.

            draw_game(win, player1_board, ball, player2_board, player1_score, player2_score)
            # draw everything.

            pygame.display.flip()
            # update the screen.

        while end == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # if the player clicks the X button, quit the game.
                    end = False
                    playAgain = False

            draw_game(win, player1_board, ball, player2_board, player1_score, player2_score)
            # draw the background.

            pygame.draw.rect(win, (255, 255, 255), (350 - 103, 300 - 103, 206, 206))
            pygame.draw.rect(win, (200, 200, 200), (250, 200, 200, 200))
            # draw the box the words are in.

            text = FINAL_FONT.render('GAME OVER', 1, (32, 32, 32))
            win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 280 - text.get_height() / 2))
            text = MAIN_FONT.render('Click to play again.', 1, (32, 32, 32))
            win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 320 - text.get_height() / 2))
            # draw the game over words.

            mousepos = pygame.mouse.get_pos()  # get the mouse position.

            if mousepos[0] > 247 and mousepos[0] < 453 and mousepos[1] > 198 and mousepos[1] < 405:  # detect in the player is hovering over the box.
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:  # if the player clicks on the box, reset the game.
                        end = False

                pygame.draw.rect(win, (0, 0, 0), (350 - 103, 300 - 103, 206, 206))
                pygame.draw.rect(win, (55, 55, 55), (250, 200, 200, 200))
                # draw the box the words are in, but invert the colours

                text = FINAL_FONT.render('GAME OVER', 1, (255, 255, 255))
                win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 280 - text.get_height() / 2))
                text = MAIN_FONT.render('Click to play again', 1, (255, 255, 255))
                win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 320 - text.get_height() / 2))
                # draw the game over words, but with the colours inverted.

            pygame.display.flip()
            # update the screen.


main(WIN, playUntil)
# run the game

pygame.quit()
quit()
# close the window
