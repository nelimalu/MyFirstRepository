#!/usr/bin/env python

'''
Minesweeper
'''

import pygame
from random import randint
import collections
# just some imports
# use "pip install pygame" in your command prompt to install pygame

pygame.font.init()  # download some fonts

WIN_WIDTH = 750
WIN_HEIGHT = 750
# set the screens size

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # create the window
pygame.display.set_caption('Minesweeper')  # set the caption

minesweeperflag = pygame.transform.scale2x(pygame.image.load('minesweeperData/minesweeperflag.png'))  # load the flag image
conversion = 50  # this variable is used to convert coordinates on the grid to pixels
recursions = 0  # this variable keeps track of recursions
main_font = pygame.font.SysFont('comicsans', 75)  # defining some fonts
final_font = pygame.font.SysFont('comicsans', 150)
gameOver = False
gameWon = False  # keep track of if the game is over

class Grid:  # creating the grid

    def __init__(self, WIN_HEIGHT, conversion):
        self.conversion = conversion
        self.sidelen = WIN_HEIGHT / self.conversion

    def draw(self, win):
        for i in range(int(self.sidelen)):  # draw the grid
            pygame.draw.rect(win, (0,0,0), (0, i * self.conversion, 750, 2))
            pygame.draw.rect(win, (0, 0, 0), (i * self.conversion, 0, 2, 750))

    def detectClicks(self, mousepos):

        coordinate = (int(mousepos[0] / self.conversion), int(mousepos[1] / self.conversion))  # convert pixels to grid coordinates
        return coordinate

class Minesweeper:

    def __init__(self, conversion, WIN_HEIGHT):
        self.conversion = conversion
        self.sidelen = int(WIN_HEIGHT / self.conversion) - 2
        self.bombs = []  # holds all the bomb locations
        self.flags = []  # holds all the flag locations
        self.excavatedCoordinates = []  # keeps track of excavated coordinates
        self.excavated = []
        self.squares = self.sidelen * self.sidelen

    def createBombs(self):  # create the bombs
        for square in range(int(self.squares / 6)):  # for a sixth of the grids squares...
            self.newbomb = (randint(0, self.sidelen), randint(0, self.sidelen))  # create a bomb
            while self.newbomb in self.bombs:  # if the bomb's coordinates match another bomb, try again
                self.newbomb = (randint(0, self.sidelen), randint(0, self.sidelen))

            self.bombs.append(self.newbomb)  # add the bomb to the list

    def createFlag(self, mousepos):  # create flags

        if mousepos not in self.flags:  # if the user didn't click on a flag...
            if [mousepos[0], mousepos[1]] not in self.excavatedCoordinates:  # if the user didn't click on an excavated coordinate...
                self.flags.append((mousepos[0], mousepos[1]))  # create a flag
        else:  # if the user clicked on a flag
            self.flags.remove((mousepos[0], mousepos[1]))  # remove the flag

    def drawBombs(self, win, colour):  # draw the bombs
        for bomb in self.bombs:
            pygame.draw.rect(win, colour, ((bomb[0] * self.conversion) + 2, (bomb[1] * self.conversion) + 2, self.conversion - 2, self.conversion - 2))
            # fill the coordinate with a colour

    def drawFlags(self, win, image):  # draw the flags
        for flag in self.flags:
            win.blit(image, (flag[0] * self.conversion + 4, flag[1] * self.conversion + 2))


    def excavate(self, mousepos, font, recursions):

        global gameOver

        if mousepos in self.bombs:  # if the user clicked on a bomb, end the game
            gameOver = True
        else:  # if the user didn't click on a bomb, excavate the area
            self.excavated.append([mousepos[0], mousepos[1], 0])
            self.excavatedCoordinates.append((mousepos[0], mousepos[1]))
        if mousepos in self.flags:  # if the player clicks on a flag, remove it
            self.flags.remove(mousepos)

        for i in self.excavated:
            if i[2] == 0:  # find how many bombs are next to it
                if (i[0] - 1, i[1]) in self.bombs: i[2] += 1
                if (i[0] + 1, i[1]) in self.bombs: i[2] += 1
                if (i[0], i[1] + 1) in self.bombs: i[2] += 1
                if (i[0], i[1] - 1) in self.bombs: i[2] += 1
                if (i[0] - 1, i[1] - 1) in self.bombs: i[2] += 1
                if (i[0] - 1, i[1] + 1) in self.bombs: i[2] += 1
                if (i[0] + 1, i[1] - 1) in self.bombs: i[2] += 1
                if (i[0] + 1, i[1] + 1) in self.bombs: i[2] += 1
            else:
                text = font.render(str(i[2]), 1, (200, 200, 200))
                win.blit(text, (i[0] * self.conversion + 12, i[1] * self.conversion + 5))  # write how many bombs are next to it


        for i in self.excavated:
            if recursions > 100:  # if the program is below 100 recursions keep going (This is a failsafe)
                break


            # This next part is written extremely badly.
            # This part makes coordinates that have 0 bordering bombs that
            # are next to eachother get excavated at the same time
            if i[:2] == [mousepos[0], mousepos[1]]:
                if i[2] == 0:

                    if (mousepos[0] - 1, mousepos[1]) not in self.bombs:
                        if mousepos[0] - 1 < 1:
                            pass
                        else:
                            if (mousepos[0] - 1, mousepos[1]) not in self.excavatedCoordinates:
                                recursions += 1
                                self.excavate((mousepos[0] - 1, mousepos[1]), font, recursions)

                    if (mousepos[0] + 1, mousepos[1]) not in self.bombs:
                        if mousepos[0] + 1 > 14:
                            pass
                        else:
                            if (mousepos[0] + 1, mousepos[1]) not in self.excavatedCoordinates:
                                recursions += 1
                                self.excavate((mousepos[0] + 1, mousepos[1]), font, recursions)
            
                    if (mousepos[0], mousepos[1] + 1) not in self.bombs:
                        if mousepos[1] + 1 > 14:
                            pass
                        else:
                            if (mousepos[0], mousepos[1] + 1) not in self.excavatedCoordinates:
                                recursions += 1
                                self.excavate((mousepos[0], mousepos[1] + 1), font, recursions)
            
                    if (mousepos[0], mousepos[1] - 1) not in self.bombs:
                        if mousepos[1] - 1 < 1:
                            pass
                        else:
                            if (mousepos[0], mousepos[1] - 1) not in self.excavatedCoordinates:
                                recursions += 1
                                self.excavate((mousepos[0], mousepos[1] - 1), font, recursions)

                    # Diagonals

                    if (mousepos[0] + 1, mousepos[1] + 1) not in self.bombs:
                        if mousepos[0] + 1 > 14 or mousepos[1] + 1 > 14:
                            pass
                        else:
                            if (mousepos[0] + 1, mousepos[1] + 1) not in self.excavatedCoordinates:
                                recursions += 1
                                self.excavate((mousepos[0] + 1, mousepos[1] + 1), font, recursions)

                    if (mousepos[0] + 1, mousepos[1] - 1) not in self.bombs:
                        if mousepos[0] + 1 > 14 or mousepos[1] - 1 < 1:
                            pass
                        else:
                            if (mousepos[0] + 1, mousepos[1] - 1) not in self.excavatedCoordinates:
                                recursions += 1
                                self.excavate((mousepos[0] + 1, mousepos[1] - 1), font, recursions)

                    if (mousepos[0] - 1, mousepos[1] + 1) not in self.bombs:
                        if mousepos[0] - 1 < 0 or mousepos[1] + 1 > 14:
                            pass
                        else:
                            if (mousepos[0] - 1, mousepos[1] + 1) not in self.excavatedCoordinates:
                                recursions += 1
                                self.excavate((mousepos[0] - 1, mousepos[1] + 1), font, recursions)

                    if (mousepos[0] - 1, mousepos[1] - 1) not in self.bombs:
                        if mousepos[0] - 1 < 0 or mousepos[1] - 1 < 0:
                            pass
                        else:
                            if (mousepos[0] - 1, mousepos[1] - 1) not in self.excavatedCoordinates:
                                recursions += 1
                                self.excavate((mousepos[0] - 1, mousepos[1] - 1), font, recursions)


    def showNumbers(self, font):

        for i in self.excavated:  # draw the amount of bombs a square is touching
            if i[2] != 0:
                text = font.render(str(i[2]), 1, (200, 200, 200))
                win.blit(text, (i[0] * self.conversion + 12, i[1] * self.conversion + 5))

    def showExcavated(self):
        for hole in self.excavated:  # make excavated coordinates brown
            pygame.draw.rect(win, (166, 123, 77), ((hole[0] * self.conversion) + 2, (hole[1] * self.conversion) + 2, self.conversion - 2, self.conversion - 2))

def redrawGameWindow(win, grid, minesweeper, flag, font, gameOver, gameWon, final_font, WIN_WIDTH):
    win.fill([100,180,100])  # make the screen green

    grid.draw(win)  # draw the grid

    minesweeper.showExcavated()  # draw the excavated spaces
    minesweeper.showNumbers(font)  # draw the numbers
    # minesweeper.drawBombs(win, (255, 64, 64)) # if you uncomment this all the bombs will be visible
    minesweeper.drawFlags(win, flag)  # draw all the placed flags
    if gameOver:  # if you clicked on a bomb...
        minesweeper.drawBombs(win, (255, 64, 64))  # show all the bombs
        minesweeper.drawFlags(win, flag)  # show all the flags
        text = final_font.render('GAME OVER', 1, (255, 255, 0))
        win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, WIN_WIDTH / 2 - text.get_height() / 2))  # print "GAME OVER"
    if gameWon:  # if you placed flags on all the bombs...
        minesweeper.drawBombs(win, (0, 0, 255))  # make all the bombs blue
        minesweeper.drawFlags(win, flag)  # draw all the flags
        text = final_font.render('YOU WIN', 1, (255, 255, 0))
        win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, WIN_WIDTH / 2 - text.get_height() / 2))  # print "YOU WIN"

    pygame.display.flip()  # update the screen

def main():

    global win, WIN_HEIGHT, conversion, minesweeperflag, main_font, gameOver, gameWon, final, recursions

    grid = Grid(WIN_HEIGHT, conversion)
    minesweeper = Minesweeper(conversion, WIN_HEIGHT)

    minesweeper.createBombs()  # make the bombs

    pressed = [1, 1, 1, 1]  # this is used to make clicks not spazz (stops a bug)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if the player clicks on the red "X" quit the program
                run = False

        mousepos = pygame.mouse.get_pos()  # get the mouse's locations
        mouse = pygame.mouse.get_pressed()  # get which mouse buttons are pressed
        gridlocation = grid.detectClicks(mousepos)  # convert the mouse location to the grid coordinates

        if mouse[0] == 1 and pressed[2] == 1:  # if the user left clicks
            if pressed[3] == 1:
                recursions = 0  # set the recursions to 0
                minesweeper.excavate(gridlocation, main_font, recursions)
                pressed[3] = 1
            else:
                pressed[3] = 0

        if not mouse[0] == 1:
            pressed[2] = 1
        else:
            pressed[2] = 0

        if mouse[2] == 1 and pressed[0] == 1:  # if the user right clicks
            if pressed[1] == 1:
                minesweeper.createFlag(gridlocation)  # create or remove a flag
                pressed[1] = 1
            else:
                pressed[1] = 0

        if not mouse[2] == 1:
            pressed[0] = 1
        else:
            pressed[0] = 0

        if collections.Counter(minesweeper.bombs) == collections.Counter(minesweeper.flags):  # if flags are placed on all the bombs end the game
            gameWon = True

        while gameOver:  # if the player clicks on a bomb...
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    gameOver = False
            # run the last screen forever
            redrawGameWindow(win, grid, minesweeper, minesweeperflag, main_font, gameOver, gameWon, final_font, WIN_WIDTH)

        while gameWon:  # if the player wins...
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    gameWon = False
            # run the last screen forever
            redrawGameWindow(win, grid, minesweeper, minesweeperflag, main_font, gameOver, gameWon, final_font, WIN_WIDTH)

        redrawGameWindow(win, grid, minesweeper, minesweeperflag, main_font, gameOver, gameWon, final_font, WIN_WIDTH)  # update the screen

if __name__ == '__main__':
    main()  # if the program is being run from the main file, run the program

pygame.quit()  # end the program
quit()