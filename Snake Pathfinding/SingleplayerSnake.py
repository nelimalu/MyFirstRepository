import pygame
from random import randint

pygame.font.init()

win_width = 750
win_height = 750

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Snake!')

conversion = 30
main_font = pygame.font.SysFont('comicsans', 50)

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

class Snake:

    def __init__(self, conversion, score):
        self.body = [[5,12], [4,12], [3,12]]
        self.conversion = conversion
        self.food = [15,12]
        self.score = score

    def draw(self, win):
        for block in self.body:
            pygame.draw.rect(win, (255, 255, 255), ((block[0] * self.conversion) + 2, (block[1] * self.conversion) + 2, self.conversion - 2, self.conversion - 2))

        pygame.draw.rect(win, (255, 0, 0), ((self.food[0] * self.conversion) + 2, (self.food[1] * self.conversion) + 2, self.conversion - 2, self.conversion - 2))

    def move(self, key):

        self.body.insert(0, [self.body[0][0] + (key == 'RIGHT' and 1) + (key == 'LEFT' and -1),self.body[0][1] + (key == 'UP' and -1) + (key == 'DOWN' and 1)])
        if self.body[0] == self.food:
            self.food = []
            while self.food == []:
                self.food = [randint(0,24), randint(0,24)]
                if self.food not in self.body:
                    break
            self.score += 1
        else:
            self.body.pop()


def redrawGameWindow(win, grid, snake, score):
    win.fill([64,64,64])
    grid.draw(win)
    snake.draw(win)

    text = main_font.render('Score: ' + str(score), 1, (200, 200, 200))
    win.blit(text, (0,0))

    pygame.display.flip()

def main():

    global win, win_height, conversion

    clock = pygame.time.Clock()
    score = 0
    grid = Grid(win_height, conversion)
    snake = Snake(conversion, score)
    key = 'RIGHT'
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        clock.tick(8)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            key = 'LEFT'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            key = 'RIGHT'
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            key = 'UP'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            key = 'DOWN'

        snake.move(key)
        if snake.body[0] in snake.body[1:]:
            break
        if snake.body[0][0] < 0 or snake.body[0][0] > 25 or snake.body[0][1] < 0 or snake.body[0][1] > 25:
            break

        redrawGameWindow(win, grid, snake, score)

if __name__ == '__main__':
    main()

pygame.quit()
quit()