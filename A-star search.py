import pygame as py
import sys
from collections import deque

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (138,43,226)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PINK = (255, 20, 147)


WINDOW_WIDTH = 600
# rows 20
rows = 30

class Node:
    def __init__(self, X, Y, parent):
        self.x = X
        self.y = Y
        self.colour = None
        self.type = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent

    def make_barrier(self):
        self.colour = BLACK
        self.type = "barrier"

    def open(self):
        self.colour = RED

    def close(self):
        self.colour = GREEN

    def make_start(self):
        self.colour = YELLOW
        self.type = "start"

    def make_end(self):
        self.colour = PURPLE
        self.type = "end"

    def make_path(self):
        self.colour = PINK

    def print(self):
        if self.colour != None:
            rect = py.Rect(self.x * cellSize, self.y * cellSize, cellSize, cellSize)
            py.draw.rect(SCREEN, self.colour, rect)
            py.draw.rect(SCREEN, BLACK, rect, 1)
            py.display.update()


def drawGrid():
    global cellSize
    cellSize = WINDOW_WIDTH // rows #Set the size of the grid block

    for x in range(0, WINDOW_WIDTH, cellSize):
        for y in range(0, WINDOW_WIDTH, cellSize):
            rect = py.Rect(x, y, cellSize, cellSize)
            py.draw.rect(SCREEN, BLACK, rect, 1)
    py.display.update()

def get_cell():
    x,y = py.mouse.get_pos()
    return  y // cellSize,  x // cellSize


def create_maze():
    maze = []
    for i in range(rows):
        col = []
        for j in range(rows):
            col.append(Node(j, i, None))
        maze.append(col)

    return maze

def draw_maze(maze):
    for y in range(rows):
        for x in range(rows):
            maze[y][x].print()

def a_star_search(maze, startNode, endNode):

    FPS = 40 #frames per second setting
    fpsClock = py.time.Clock()

    print(startNode.x, endNode.x)
    openList = deque([])
    closedList = deque([])


    openList.append(startNode)

    while len(openList) > 0:
        
        min = openList[0]
        
        for i in range(len(openList)):
        
            if openList[i].f < min.f:
                min = openList[i]

        currentNode = min
        openList.remove(currentNode)

        currentNode.close()
        closedList.append(currentNode)

        #print(currentNode[0].x, currentNode[0].y)

        if (currentNode.x == endNode.x) and (currentNode.y == endNode.y):
            print("You found the end")

            # make path
            while currentNode:
                currentNode.make_path()
                currentNode = currentNode.parent

            startNode.make_start()
            endNode.make_end() 
            return maze


        def generate_children():
            children = []
            directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 0], [-1, 0]]

            for dir in directions:
                x = currentNode.x #column pos 
                y = currentNode.y #row pos 
                temp_x = x + dir[1]
                temp_y = y + dir[0]

                if((0 <= temp_x <= (rows - 1)) and (0 <= temp_y <= (rows - 1))):

                    if maze[temp_y][temp_x].type == ("barrier") or maze[temp_y][temp_x].type == ("start"):
                        continue

                    else:
                        if ((dir == [0, 1]) and (x < rows)) or (dir == [0, -1] and \
                            (x > 0)) or (dir == [1, 0] and (y < rows)) or (dir == [-1, 0] and (y > 0)):
                                    
                            children.append(maze[temp_y][temp_x])
                    
            #print(len(children))
            return children

        children = generate_children()

        def get_distance(child, endNode):
            dist = pow((child.x - endNode.x), 2) + pow((child.y - endNode.y), 2)
            return dist

        for child in children:
            if child in closedList:
                continue

            child.g = currentNode.g + 1
            child.h = get_distance(child, endNode)
            child.f = child.g + child.h
            
            #Child is already in openList
            for open_node in openList:
                if child.g > open_node.g:
                    continue

            # Add the child to the openList
            child.open()
            child.parent = currentNode
            openList.append(child)

         # Update the screen
        draw_maze(maze)
        fpsClock.tick(FPS)

def draw_barrier(maze, row, col):
    max = rows
    if (row < max and col < max):
        if not (maze[row][col].type == "start" or maze[row][col].type == "end"):
            maze[row][col].make_barrier()
    
    return maze

def main():
    global SCREEN
    py.init()
    SCREEN = py.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
    SCREEN.fill(WHITE)
    py.display.set_caption('A* Search')

    drawGrid()
    maze =create_maze()

    start = True
    end = False
    getUserInput = True
    startNode = None
    endNode = None
    run_search = True

    while True:
 
        for event in py.event.get():
            if getUserInput:
                row, col = get_cell()
                if py.mouse.get_pressed()[0]:
                   maze = draw_barrier(maze, row, col)

                if event.type == py.MOUSEBUTTONDOWN:
                    if event.button == 1: # 1 == left button

                        if start:
                            maze[row][col].make_start()
                            startNode = maze[row][col]
                            start = False
                            end = True

                        elif end:
                            maze[row][col].make_end()
                            endNode = maze[row][col]
                            end = False


                    if event.button == 3: #stop accepting blocks from user
                        getUserInput = False      
                
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    run_search = True
                    getUserInput = True
                    main()


            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if (not getUserInput) and run_search:
                maze = a_star_search(maze, startNode, endNode)
                run_search = False

        draw_maze(maze)
        
main()
