import pygame

win_width = 750
win_height = 750

win = pygame.display.set_mode((win_height, win_width))
pygame.display.set_caption('Grid!')

conversion = 30

# make a mini version of the code run again to get absolute shortest distance

class Grid:

    def __init__(self, win_height, conversion):
        self.win_height = win_height
        self.sidelen = win_height / conversion
        self.conversion = conversion

    def draw(self, win):

        for i in range(int(self.sidelen)):
            pygame.draw.rect(win, (0, 0, 0), (0, i * self.conversion, 800, 2))
            pygame.draw.rect(win, (0, 0, 0), (i * self.conversion, 0, 2, 800))

    def paint(self, mousepos):

        box = (int(mousepos[0] / self.conversion) * self.conversion, int(mousepos[1] / self.conversion) * self.conversion)
        return box


def redrawGameWindow(win, grid, filledBoxes, conversion):

    win.fill([255, 255, 255])
    grid.draw(win)

    for box in filledBoxes:
        pygame.draw.rect(win, (64, 64, 64), (box[0], box[1], conversion, conversion))

    pygame.display.flip()


def main():

    global win, win_height, conversion

    run = True
    grid = Grid(win_height, conversion)
    filledBoxes = []
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        clicks = pygame.mouse.get_pressed()
        if clicks[0] == 1:
            mousepos = pygame.mouse.get_pos()
            if grid.paint(mousepos) not in filledBoxes:
                filledBoxes.append(grid.paint(mousepos))
        elif clicks[2] == 1:
            mousepos = pygame.mouse.get_pos()
            if grid.paint(mousepos) in filledBoxes:
                filledBoxes.remove(grid.paint(mousepos))
        else:
            mousepos = None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            filledBoxes = []

        redrawGameWindow(win, grid, filledBoxes, conversion)


if __name__ == '__main__':
    main()

pygame.quit()
quit()