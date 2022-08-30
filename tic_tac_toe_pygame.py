import pygame
import numpy
import time

from pygame.constants import SRCCOLORKEY

pygame.init()
pygame.font.init()
pygame.display.set_caption("Tic-tac-toe")

#variables
rc_num = 15 # size of table
row_lines = []
column_lines = []
mouse_pos = (0,0)
grid =[]
move = (numpy.inf, numpy.inf)
reason = ""

#CONSTANTS
WIDTH, HEIGHT = 700,700
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (66,144,245)
SPACE = WIDTH / rc_num
GAME_FONT = pygame.font.SysFont("comicsans", int(SPACE*1.75))
FONT = pygame.font.SysFont("comicsans", 75)

CI = "O"
CR = "X"
A = 5 # number of chars needed for win
B = A -1
CIRCLES = "O"*A
CROSSES = "X"*A
CIR = "O"*B
CROSS = "X"*B 
X_TEXT = GAME_FONT.render(CR, 0,(255,0,0))
O_TEXT = GAME_FONT.render(CI, 0,(0,255,0))


#INIT

    #rows and columns positions
for i in range(rc_num +1):
    row_lines.append((0, int(i*SPACE)))
    column_lines.append((int(i*SPACE), 0))

    #grid init
g = []
for j in range(rc_num):
    for i in range(rc_num):
        g.append("-")

    grid.append(g)
    g = []


    #window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#TIC TAC TOE func definition
def draw_grid():
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(grid[i][j], end = ' ')
        print()
    print()

def is_winner(symbol, grid):
    is_winner = True

    #rows
    string  = ""
    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            string += grid[i][j]

        if symbol in string:
            is_winner = False
        string = ""

    #columns
    string = ""
    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            string += grid[j][i]

        if symbol in string:
            is_winner = False
        string = ""

    #diagonals from top left to  upper right
    string = ""
    range_num = len(grid[0])
    iter_num = 0
    for i in range(range_num):
        for j in range(range_num):
            string += grid[j][j + iter_num]

        if symbol in string:
            is_winner = False
        string = ""
        iter_num += 1
        range_num -= 1
        
    #diagonals from top left to lower right
    string = ""
    range_num = len(grid[0])
    iter_num = 0
    for i in range(range_num):
        for j in range(range_num):
            string += grid[j + iter_num][j]

        if symbol in string:
            is_winner = False
        string = ""
        iter_num += 1
        range_num -= 1


    #diagonals from top right to top left 
    string = ""
    range_num = len(grid[0])
    iter_num = 0
    for i in range(range_num):
        for j in range(range_num):
            string += grid[j][-(j + iter_num)]

        if symbol in string:
            is_winner = False
        string = ""
        iter_num += 1
        range_num -= 1

    #diagonals from top right to lower right
    string = ""
    range_num = len(grid[0])
    iter_num = 0
    for i in range(range_num):
        for j in range(range_num):
            string += grid[j + iter_num][-j]

        if symbol in string:
            is_winner = False
        string = ""
        iter_num += 1
        range_num -= 1

    return is_winner


def tie_game():
    tie = False
    for j in grid:
        for i in j:
            if i == "-":
                return tie

    tie = True
    return tie

#PYGAME func definition
def draw():
    screen.fill(WHITE)
    positions = []
    #drawing lines
    for i, j in zip(row_lines, column_lines):
        pygame.draw.line(screen, BLACK, i, (WIDTH, i[1]), 1)
        pygame.draw.line(screen, BLACK, j, (j[0], HEIGHT), 1)

    for i, x in enumerate(grid):
        for j, y in enumerate(x):
            if y == CR:
                screen.blit(X_TEXT, (j*SPACE + 6, i*SPACE))
            if y == CI:
                screen.blit(O_TEXT, (j*SPACE + 3, i*SPACE))


    pygame.display.update()

def draw_game_over(reason):
    text = ""
    if reason == "o_win":
        text = "O wins!"
    if reason == "x_win":
        text = "X wins!"
    if reason == "tie_game":
        text = "Tie game!"

    notify = FONT.render("GAME OVER - " + str(text), 1, BLUE)
    screen.blit(notify, (WIDTH/2 - notify.get_width()/2,HEIGHT/2 - notify.get_height()/2))
    pygame.display.update()
    time.sleep(5)

    

def get_rc(pos):
    x = pos[0]
    y = pos[1]

    valid = True
    row = numpy.inf
    column = numpy.inf

    for i in range(rc_num):
        tup_1 = row_lines[i]
        tup_2 = row_lines[i+1]
        if y > tup_1[1] and  y < tup_2[1]:
            row = int(i)       
            break

    for i in range(rc_num):
        tup_1 = column_lines[i]
        tup_2 = column_lines[i+1]
        if x > tup_1[0] and  x < tup_2[0]:
            column = int(i)
            break

    #checking if the value is valid
    if type(row) != int or type(column) != int:
        valid = False

    if type(row) == int and type(column) == int:
        if grid[row][column] != "-":
            valid = False

    tup = (row, column)
    return valid, tup

def main():
    run = True
    SYMBOL = CR
    division_rest = 0
    division_index = 0
    winner = ""
    game_over = True
    draw()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                valid = True
                mouse_pos = pygame.mouse.get_pos()
                valid, move = get_rc(mouse_pos)
                if valid: #switching between O and X
                    division_index += 1
                    division_rest = division_index % 2
                    if division_rest == 1:
                        SYMBOL = CR
                    else:
                        SYMBOL = CI
                    grid[move[0]][move[1]] = SYMBOL
                    draw_grid()
                    draw()


                    game_over = is_winner(CIRCLES, grid)
                    if game_over == False:
                        reason = "o_win"
                        break

                    game_over = is_winner(CROSSES, grid)
                    if game_over == False:
                        reason = "x_win"
                        break

                    if tie_game():
                        game_over = False
                        reason = "tie_game"
                        break
                else:
                    print("invalid value")  


        if game_over == False:  
            draw_game_over(reason)
            run = False
main()  
pygame.quit()
