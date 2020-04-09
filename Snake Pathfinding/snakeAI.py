import pygame
from queue import PriorityQueue
from random import randint
# a couple of imports
# use "pip install pygame" in the command prompt to install pygame

pygame.font.init()  # download some fonts

win_width = 750
win_height = 750
# set up the screen size

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Snake!')
# set up the window

conversion = 30  # this is used to convert from blocks in the grid to pixels
main_font = pygame.font.SysFont('comicsans', 50)  # a font that is used to display the score.
path_show = []  # variable used to speed up the program with the pathfinding.
score = 0  # keeps track of the scores

class Grid:

    def __init__(self, win_height, conversion):
        self.win_height = win_height
        self.sidelen = win_height / conversion * 2
        self.conversion = conversion

    def draw(self, win):

        for i in range(int(self.sidelen)):
            pygame.draw.rect(win, (32, 32, 32), (0, i * self.conversion, 800, 2))  # draw the grid
            pygame.draw.rect(win, (32, 32, 32), (i * self.conversion, 0, 2, 800))

    def paint(self, mousepos):  # this function takes the mouse position and fills in the box the mouse is in

        box = (int(mousepos[0] / self.conversion) * self.conversion, int(mousepos[1] / self.conversion) * self.conversion)
        return box


class State(object):  # class that defines basic things for almost all a* algorithms. This is the base class.

    def __init__(self, value, parent,
                 start=0,
                 goal=0):

        self.children = []  # this carries all of the neighboring possibilities
        self.parent = parent  # this is the current location that is locating the children
        self.value = value  # the current state of the word
        self.dist = 0  # the distance from the start to finish

        if parent:  # if there is a parent...
            self.start = parent.start  # the start is the location of the parent
            self.goal = parent.goal  # the end is the goal of the parent.
            self.path = parent.path[:]  # the path is all of the previous steps taken by previous parents.
            self.path.append(value)  # add the location of the parent to the path.
        else:  # if there is no parent...
            self.path = [value]  # the path is the starting location
            self.start = start  # The start is self.start
            self.goal = goal  # the end is self.end

    def GetDistance(self):  # outlining some functions that will be defined later.
        pass

    def CreateChildren(self):
        pass
class State_String(State):  # a class to set up the a* algorithm, but more personalized for the problem.
    def __init__(self, value, parent, start=0, goal=0):  # define things from the previous class.

        super(State_String, self).__init__(value, parent, start, goal)  # makes it so you can call the base class.
        self.dist = self.GetDistance()

    def GetDistance(self):  # get the distance from the current location to the endpoint.

        if self.value == self.goal:  # if you reached the endpoint, return 0 as the distance.
            return 0

        return abs(self.value[0] - self.goal[0]) + abs(self.value[1] - self.goal[1])
        # subtract the current x,y from the goal x,y and make it the absolute value

    def CreateChildren(self, snake):  # create the children of the current parent

        global conversion, win_height, win_width, path_show  # some global variables

        # this part hasn't gotten any better.
        if not self.children:
            val = (self.value[0] - 1, self.value[1])  # make the new child based on the current one.
            print(snake.body)
            if [val[0], val[1]] not in snake.body:  # prevents the snake from going into itself
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:  # prevents going over the screen
                    child = State_String(val, self)  # make a new child.
                    self.children.append(child)  # add the new child to the list of children.

            val = (self.value[0] + 1, self.value[1])
            if [val[0], val[1]] not in snake.body:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    child = State_String(val, self)
                    self.children.append(child)

            val = (self.value[0], self.value[1] - 1)
            if [val[0], val[1]] not in snake.body:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    child = State_String(val, self)
                    self.children.append(child)

            val = (self.value[0], self.value[1] + 1)
            if [val[0], val[1]] not in snake.body:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    child = State_String(val, self)
                    self.children.append(child)

def redrawGameWindow(win, grid, snake, score):
    win.fill([64,64,64])  # make the background gray
    grid.draw(win)  # draw the grid

    snake.draw(win)  # draw the snake

    text = main_font.render('Score: ' + str(score), 1, (200, 200, 200))  # display the score
    win.blit(text, (0,0))

    pygame.display.flip()  # update the screen

class Snake:

    def __init__(self, conversion):
        self.body = [[5,12], [4,12], [3,12]]  # this is the snake's initial position
        self.conversion = conversion  # this variable is used to convert from the grid coordinates to pixels
        self.goal = [15,12]  # this is the initial position of the food
        self.path = []  # this holds the current path from the start to the current position.
        self.visitedQueue = []  # keeps track of all children that have been looked at so it doesnt look at one twice.
        self.priorityQueue = PriorityQueue()  # a list that orders things in order of importance.
        self.start = self.body[0]  # the start position of the algorithm is the snake's head

    def draw(self, win):

        for block in self.body:  # draw the snake
            pygame.draw.rect(win, (255, 255, 255), ((block[0] * self.conversion) + 2, (block[1] * self.conversion) + 2, self.conversion - 2, self.conversion - 2))

        pygame.draw.rect(win, (200, 200, 200), ((self.body[0][0] * self.conversion) + 2, (self.body[0][1] * self.conversion) + 2, self.conversion - 2, self.conversion - 2))
        # make the head of the snake slightly darker

        pygame.draw.rect(win, (255, 0, 0), ((self.goal[0] * self.conversion) + 2, (self.goal[1] * self.conversion) + 2, self.conversion - 2, self.conversion - 2))
        # draw the food

    def move(self, key):

        global score

        self.body.insert(0, [self.body[0][0] + (key == 'RIGHT' and 1) + (key == 'LEFT' and -1),self.body[0][1] + (key == 'UP' and -1) + (key == 'DOWN' and 1)])  # move the snake
        if self.body[0] == self.goal:  # if the snake ate the food...
            self.goal = []
            while self.goal == []:
                self.goal = [randint(0,24), randint(0,24)]  # pick a new spot
                if self.goal in self.body:  # if the new spot is inside the snake try again
                    self.goal = []
            score += 1  # add one to the score
            self.start = self.body[0]  # the new startpoint is the head of the snake
            self.priorityQueue.queue.clear()  # clear the priority queue
            self.visitedQueue = []  # clear the visited queue
            self.Solve()  # find the path
            self.path = self.path[1:]  # this prevents the snake from going into itself
        else:
            self.body.pop()  # if the snake doesn't eat food, remove the last block in the snake (don't make the snake grow)

    def Solve(self):
        startState = State_String(self.start,  # starting point
                                  0,  # no current parent
                                  self.start,
                                  self.goal)
        # how the algorithm begins

        global win, win_height, conversion, path_show, score

        grid = Grid(win_height, conversion)

        count = 0  # keeps track of iterations
        self.priorityQueue.put((0, count, startState))  # [2] keeps track of everything, other two are not important
        self.path = []

        while (not self.path and self.priorityQueue.qsize()):  # while the path and Priority Queue aren't empty

            closestChild = self.priorityQueue.get()[2]  # get the child closest to the final answer.
            if closestChild.value in self.visitedQueue:  # prevents going to the same spot twice.
                continue
            if (closestChild.value[0] * conversion, closestChild.value[1] * conversion) not in path_show:  # speed up the program
                path_show.append((closestChild.value[0] * conversion, closestChild.value[1] * conversion))   # keep a copy of the entire path
            closestChild.CreateChildren(self)  # make children out of that closest child.
            self.visitedQueue.append(closestChild.value)  # add that child to the visited queue

            for event in pygame.event.get():  # if the user presses the 'x' button, quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            for child in closestChild.children:  # for every child in the closest child's children.
                if child.value not in self.visitedQueue:  # if their location is not in the visited queue
                    count += 1  # add one to the count
                    if child.dist == 0:  # if the child has reached the final answer, stop the loop
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist, count, child))  # add the new child to the Priority Queue

            redrawGameWindow(win, grid, self, score)  # draw the screen

        if not self.path:  # if there is no possible path...
            while True:
                for event in pygame.event.get():  # if the user presses the 'x' button, quit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                redrawGameWindow(win, grid, self, score)  # draw the screen

        return self.path  # return the path from the head to the apple

def main():

    global win, win_height, conversion, score

    clock = pygame.time.Clock()  # this controls the frames per second
    grid = Grid(win_height, conversion)  # create the grid
    snake = Snake(conversion)  # create the snake
    key = 'RIGHT'  # make the snake begin moving right
    run = True
    while run:
        for event in pygame.event.get():  # if the user clicks the 'x' button, quit
            if event.type == pygame.QUIT:
                run = False

        clock.tick(8)  # run at 8 frames per second

        for i in snake.path:  # follow the path provided by the algorithm
            if snake.body[0][0] - 1 == i[0] and snake.body[0][1] == i[1]:
                key = 'LEFT'
            elif snake.body[0][0] + 1 == i[0] and snake.body[0][1] == i[1]:
                key = 'RIGHT'
            elif snake.body[0][1] - 1 == i[1] and snake.body[0][0] == i[0]:
                key = 'UP'
            elif snake.body[0][1] + 1 == i[1] and snake.body[0][0] == i[0]:
                key = 'DOWN'

        snake.move(key)  # move the snake

        if snake.body[0] in snake.body[1:]:  # quit if the snake goes into itself
            break
        if snake.body[0][0] < 0 or snake.body[0][0] > 25 or snake.body[0][1] < 0 or snake.body[0][1] > 25:  # quit if the snake leaves the screen
            break

        redrawGameWindow(win, grid, snake, score)  # update the screen

if __name__ == '__main__':  # check if the program is being run from the base file
    main()  # run the program

pygame.quit()  # end the program
quit()