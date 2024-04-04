import sys
import pygame as pg
from pygame.locals import QUIT, MOUSEBUTTONDOWN

### Global Variables
player_char = 'x'
'''Player character: x or o'''

winner = None
draw = None
WIDTH = 600
HEIGHT = 600
background_color = (255, 255, 255)
line_color = (0, 0, 0)

board = [[None]*3, [None]*3, [None]*3]
'''3x3 Board to store x/o values for each cell'''


def reset_game():
    global board, winner, player_char, draw
    time.sleep(3)
    player_char = 'x'
    draw = False
    winner = None
    board = [[None]*3, [None]*3, [None]*3]
    board_init(screen)


def draw_x(line_color, screen, clicked_row, clicked_col):
    pg.draw.line(screen, line_color, (clicked_col*(WIDTH/3)+WIDTH*0.05, clicked_row*(HEIGHT/3)+HEIGHT*0.05), ((clicked_col+1)*(WIDTH/3)-WIDTH*0.05, (clicked_row+1)*(HEIGHT/3)-HEIGHT*0.05), 7)
    pg.draw.line(screen, line_color, ((clicked_col+1)*(WIDTH/3)-WIDTH*0.05, clicked_row *
                 (HEIGHT/3)+HEIGHT*0.05), (clicked_col*(WIDTH/3)+WIDTH*0.05, (clicked_row+1)*(HEIGHT/3)-HEIGHT*0.05), 7)

def draw_o(line_color, screen, clicked_row, clicked_col):
    pg.draw.circle(screen, line_color, (int(clicked_col*(WIDTH/3)+WIDTH/6), int(clicked_row*(HEIGHT/3)+HEIGHT/6)), WIDTH/6-WIDTH*0.05, 7)
    
def check_win(board):
    global winner, draw
    # Check for win in rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != None:
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0),
                (0, (row + 1)*HEIGHT / 3 - HEIGHT / 6),
                (WIDTH, (row + 1)*HEIGHT / 3 - HEIGHT / 6),
                4)
            break
    # Check for win in columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != None:
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0),
                ((col + 1)*WIDTH / 3 - WIDTH / 6, 0),
                ((col + 1)*WIDTH / 3 - WIDTH / 6, HEIGHT),
                4)
            break
    # Check for win in diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != None:
        winner = board[0][0]
        pg.draw.line(screen, (250, 0, 0), (0, 0), (WIDTH, HEIGHT), 4)
        game_over()
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != None:
        winner = board[0][2]
        pg.draw.line(screen, (250, 0, 0), (0, HEIGHT), (WIDTH, 0), 4)
    # Check for draw
    if all([cell != None for row in board for cell in row]) and winner == None:
        draw = True
if __name__ == '__main__':
    pg.init()
    CLOCK = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Tic Tac Toe')
    screen.fill(background_color)
    
    # Draw board grid
    pg.draw.line(screen, line_color, (WIDTH/3, 0), (WIDTH/3, HEIGHT), 7)
    pg.draw.line(screen, line_color, (WIDTH/3*2, 0), (WIDTH/3*2, HEIGHT), 7)
    pg.draw.line(screen, line_color, (0, HEIGHT/3), (WIDTH, HEIGHT/3), 7)
    pg.draw.line(screen, line_color, (0, HEIGHT/3*2), (WIDTH, HEIGHT/3*2), 7)

    # Game loop
    # Draw X or O on the board on mouse click
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Get the row and column of the clicked cell
                mouseX, mouseY = pg.mouse.get_pos()
                clicked_row = int(mouseY // (HEIGHT/3))
                clicked_col = int(mouseX // (WIDTH/3))
                # Check if the cell is empty then draw X or O
                if board[clicked_row][clicked_col] == None:
                    if player_char == 'x':
                        draw_x(line_color, screen, clicked_row, clicked_col)
                        board[clicked_row][clicked_col] = 'x'
                        player_char = 'o'
                    else:
                        draw_o(line_color, screen, clicked_row, clicked_col)
                        board[clicked_row][clicked_col] = 'o'
                        player_char = 'x'
                    print(board)
        pg.display.update() 
        CLOCK.tick(30)