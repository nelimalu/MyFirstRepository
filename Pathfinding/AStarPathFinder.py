import pygame  # this is used to make the grid and display
from queue import PriorityQueue  # this is for the pathfinding algorithm
from random import randint  # this is for choosing the start and end points.

win_width = 750
win_height = 750
# define the screen

win = pygame.display.set_mode((win_height, win_width))
pygame.display.set_caption('a* Pathfinding Algorithm')

conversion = 30  # this is the conversion from points on the grid to pixels on the screen.
filledBoxes = []  # this holds the barriers
path_show = []  # this holds the entire path.


class Grid:

    def __init__(self, win_height, conversion):
        self.win_height = win_height
        self.sidelen = win_height / conversion * 2
        self.conversion = conversion

    def draw(self, win):

        for i in range(int(self.sidelen)):
            pygame.draw.rect(win, (0, 0, 0), (0, i * self.conversion, 800, 2))  # draw the grid
            pygame.draw.rect(win, (0, 0, 0), (i * self.conversion, 0, 2, 800))

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

    def CreateChildren(self):  # create the children of the current parent

        global filledBoxes, conversion, win_height, win_width, path_show  # some global variables

        # brace yourself this part is written extremely badly.
        if not self.children:
            val = (self.value[0] - 1, self.value[1])  # make the new child based on the current one.
            if (val[0] * conversion, val[1] * conversion) not in filledBoxes:  # prevents going through the barriers
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:  # prevents going over the screen
                    if val not in self.path:  # prevents looking at the same coordinate twice
                        child = State_String(val, self)  # make a new child.
                        self.children.append(child)  # add the new child to the list of children.

            val = (self.value[0] + 1, self.value[1])
            if (val[0] * conversion, val[1] * conversion) not in filledBoxes:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    if val not in self.path:
                        child = State_String(val, self)
                        self.children.append(child)

            val = (self.value[0], self.value[1] - 1)
            if (val[0] * conversion, val[1] * conversion) not in filledBoxes:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    if val not in self.path:
                        child = State_String(val, self)
                        self.children.append(child)

            val = (self.value[0], self.value[1] + 1)
            if (val[0] * conversion, val[1] * conversion) not in filledBoxes:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    if val not in self.path:
                        child = State_String(val, self)
                        self.children.append(child)

            # diagonals

            val = (self.value[0] - 1, self.value[1] - 1)
            if (val[0] * conversion, val[1] * conversion) not in filledBoxes:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    if val not in self.path:
                        child = State_String(val, self)
                        self.children.append(child)

            val = (self.value[0] - 1, self.value[1] + 1)
            if (val[0] * conversion, val[1] * conversion) not in filledBoxes:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    if val not in self.path:
                        child = State_String(val, self)
                        self.children.append(child)

            val = (self.value[0] + 1, self.value[1] - 1)
            if (val[0] * conversion, val[1] * conversion) not in filledBoxes:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    if val not in self.path:
                        child = State_String(val, self)
                        self.children.append(child)

            val = (self.value[0] + 1, self.value[1] + 1)
            if (val[0] * conversion, val[1] * conversion) not in filledBoxes:
                if val[0] * conversion > -1 and val[0] * conversion < win_width and val[1] * conversion > -1 and val[1] * conversion < win_height:
                    if val not in self.path:
                        child = State_String(val, self)
                        self.children.append(child)




class main:  # the actual thing
    def __init__(self, start, goal):  # what is the start point and end point.

        self.path = []  # this holds the current path from the start to the current position.
        self.visitedQueue = []  # keeps track of all children that have been looked at so it doesnt look at one twice.
        self.priorityQueue = PriorityQueue()  # a list that orders things in order of importance.
        self.start = start
        self.goal = goal

    def Solve(self):
        startState = State_String(self.start,  # starting point
                                  0,  # no current parent
                                  self.start,
                                  self.goal)
        # how the algorithm begins

        global win, win_height, conversion, filledBoxes, path_show

        run = True
        grid = Grid(win_height, conversion)
        clock = pygame.time.Clock()

        count = 0  # keeps track of iterations
        self.priorityQueue.put((0, count, startState))  # [2] keeps track of everything, other two are not important

        while (not self.path and self.priorityQueue.qsize()):  # while the path and Priority Queue aren't empty
            # clock.tick(6)

            closestChild = self.priorityQueue.get()[2]  # get the child closest to the final answer.
            if closestChild.value in self.visitedQueue:  # prevents going to the same spot twice.
                continue
            if (closestChild.value[0] * conversion, closestChild.value[1] * conversion) not in path_show:
                path_show.append((closestChild.value[0] * conversion, closestChild.value[1] * conversion))  # show the path
            closestChild.CreateChildren()  # make children out of that closest child.
            self.visitedQueue.append(closestChild.value)  # add that child to the visited queue

            for event in pygame.event.get():  # if the user presses the 'x' button, quit
                if event.type == pygame.QUIT:
                    run = False

            for child in closestChild.children:  # for every child in the closest child's children.
                if child.value not in self.visitedQueue:  # if their location is not in the visited queue
                    count += 1  # add one to the count
                    if child.dist == 0:  # if the child has reached the final answer, stop the loop
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist, count, child))  # add the new child to the Priority Queue

            redrawGameWindow(win, grid, filledBoxes, conversion, path_show, start, goal, closestChild, [])  # draw the screen

        return self.path  # return the final path (the pink line)


def drawing(start, goal):

    global win, win_height, conversion, filledBoxes

    run = True
    grid = Grid(win_height, conversion)
    filledBoxes = []
    while run:
        for event in pygame.event.get():  # if the player clicks the "x" button, quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        clicks = pygame.mouse.get_pressed()  # detect mouse clicks
        if clicks[0] == 1:
            mousepos = pygame.mouse.get_pos()
            if grid.paint(mousepos) not in filledBoxes and grid.paint(mousepos) != (start[0] * conversion, start[1] * conversion) and grid.paint(mousepos) != (goal[0] * conversion, goal[1] * conversion):
                filledBoxes.append(grid.paint(mousepos))  # add the barriers
        elif clicks[2] == 1:
            mousepos = pygame.mouse.get_pos()
            if grid.paint(mousepos) in filledBoxes:
                filledBoxes.remove(grid.paint(mousepos))  # remove the barriers
        else:
            mousepos = None

        keys = pygame.key.get_pressed()  # detect keypresses
        if keys[pygame.K_r]:  # if the player presses "r", remove all the barriers
            filledBoxes = []

        if keys[pygame.K_RETURN]:  # if the player hits the return key, begin the algorithm
            break

        redrawGameWindow(win, grid, filledBoxes, conversion, [], start, goal, [], [])  # draw the screen


def final(start, goal, a):  # once the program is done display the path
    run = True

    grid = Grid(win_height, conversion)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        redrawGameWindow(win, grid, filledBoxes, conversion, [], start, goal, [], a)


def redrawGameWindow(win, grid, filledBoxes, conversion, path_show, start, goal, closestChild, a):

    win.fill([255, 255, 255])  # make the background white
    grid.draw(win)  # draw the grid


    for box in filledBoxes:
        pygame.draw.rect(win, (64, 64, 64), (box[0], box[1], conversion, conversion))  # draw the barriers

    for value in path_show:
        pygame.draw.rect(win, (50, 205, 50), (value[0], value[1], conversion, conversion))  # draw the path in greens

    try:
        for block in a.path:
            pygame.draw.rect(win, (255,192,203), (block[0] * conversion, block[1] * conversion, conversion, conversion))  # draw the final path in pink
    except:
        pass

    pygame.draw.rect(win, (255, 0, 0), (start[0] * conversion, start[1] * conversion, conversion, conversion))  # draw the start point
    pygame.draw.rect(win, (0, 0, 255), (goal[0] * conversion, goal[1] * conversion, conversion, conversion))  # draw the end point

    try:
        pygame.draw.rect(win, (0, 255, 20), (closestChild.value[0] * conversion, closestChild.value[1] * conversion, conversion, conversion))  # draw the closest child's position
    except:
        pass

    pygame.display.flip()  # update the screen

if __name__ == '__main__':

    start = (randint(0, 24),randint(0, 24))  # pick the start and endpodints
    goal = (randint(0, 24),randint(0, 24))

    # start = (12,13)
    # goal = (5,0)

    a = main(start, goal)  # define the start and end for the algorithm.
    drawing(start, goal)  # begin drawing
    a.Solve()  # run the algorithm.
    final(start, goal, a)  # display the final path

    for i in range(len(a.path)):
        print("{0}) {1}".format(i, a.path[i]))  # print out the path.


pygame.quit()  # end the program
quit()