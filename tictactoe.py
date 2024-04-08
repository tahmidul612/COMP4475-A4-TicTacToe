import sys
import time
import pygame as pg
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import minimax

# Global Variables
player_char = 'x'
'''Player character: x or o'''

winner = None
draw = None
WIDTH = 600
HEIGHT = 600
background_color = (255, 255, 255)
line_color = (0, 0, 0)
game_running = False

board = [[None]*3, [None]*3, [None]*3]
'''3x3 Board to store x/o values for each cell'''


def reset_game():
    global board, winner, player_char, draw, game_running
    time.sleep(3)
    player_char = 'x'
    draw = False
    winner = None
    board = [[None]*3, [None]*3, [None]*3]
    game_running = False
    menu()


def draw_x(line_color, screen, clicked_row, clicked_col):
    pg.draw.line(screen, line_color, (clicked_col*(WIDTH/3)+WIDTH*0.05, clicked_row*(HEIGHT/3) +
                 HEIGHT*0.05), ((clicked_col+1)*(WIDTH/3)-WIDTH*0.05, (clicked_row+1)*(HEIGHT/3)-HEIGHT*0.05), 7)
    pg.draw.line(screen, line_color, ((clicked_col+1)*(WIDTH/3)-WIDTH*0.05, clicked_row *
                 (HEIGHT/3)+HEIGHT*0.05), (clicked_col*(WIDTH/3)+WIDTH*0.05, (clicked_row+1)*(HEIGHT/3)-HEIGHT*0.05), 7)


def draw_o(line_color, screen, clicked_row, clicked_col):
    pg.draw.circle(screen, line_color, (int(clicked_col*(WIDTH/3)+WIDTH/6),
                   int(clicked_row*(HEIGHT/3)+HEIGHT/6)), WIDTH/6-WIDTH*0.05, 7)


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
            game_over()
            break
    # Check for win in columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != None:
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0),
                         ((col + 1)*WIDTH / 3 - WIDTH / 6, 0),
                         ((col + 1)*WIDTH / 3 - WIDTH / 6, HEIGHT),
                         4)
            game_over()
            break
    # Check for win in diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != None:
        winner = board[0][0]
        pg.draw.line(screen, (250, 0, 0), (0, 0), (WIDTH, HEIGHT), 4)
        game_over()
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != None:
        winner = board[0][2]
        pg.draw.line(screen, (250, 0, 0), (0, HEIGHT), (WIDTH, 0), 4)
        game_over()
    # Check for draw
    if all([cell != None for row in board for cell in row]) and winner == None:
        draw = True
        game_over()


def game_over():
    global winner, draw
    font = pg.font.Font(None, 48)
    if winner or draw:
        if winner:
            msg = str(f'{winner} wins!')
        else:
            msg = str('It\'s a draw!')
        text = font.render(msg, True, (255, 255, 255))
        screen.fill((0, 0, 0), (0, HEIGHT/2-50, WIDTH, 100))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)
        pg.display.update()
        reset_game()


def board_init(algorithm, background_color=background_color, line_color=line_color):
    global game_running
    game_running = True
    font = pg.font.Font(None, 48)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Tic Tac Toe')
    screen.fill(background_color)
    # Draw board grid
    pg.draw.line(screen, line_color, (WIDTH/3, 0), (WIDTH/3, HEIGHT), 7)
    pg.draw.line(screen, line_color, (WIDTH/3*2, 0), (WIDTH/3*2, HEIGHT), 7)
    pg.draw.line(screen, line_color, (0, HEIGHT/3), (WIDTH, HEIGHT/3), 7)
    pg.draw.line(screen, line_color, (0, HEIGHT/3*2), (WIDTH, HEIGHT/3*2), 7)
    
    ai_char = 'o' if player_char == 'x' else 'x'
    ai = minimax.MiniMax(board, ai_char, player_char) if algorithm == 'minimax' else mcts.MCTS(board, ai_char, player_char)
    # Game loop
    # Draw X or O on the board on mouse click
    while game_running:
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
                    turn(board, screen, clicked_row, clicked_col)
                    turn(board, screen, *ai.bestMove(board))
        pg.display.update()
        clock.tick(30)


def turn(board, screen, clicked_row, clicked_col):
    global player_char
    if board[clicked_row][clicked_col] == None:
        if player_char == 'x':
            draw_x(line_color, screen, clicked_row, clicked_col)
            board[clicked_row][clicked_col] = 'x'
            player_char = 'o'
        else:
            draw_o(line_color, screen, clicked_row, clicked_col)
            board[clicked_row][clicked_col] = 'o'
            player_char = 'x'
        check_win(board)


def menu():
    global game_running
    screen.fill((20, 20, 20))
    game_running = False
    button_w, button_h = WIDTH*0.5, 50
    Button(WIDTH/2-button_w/2, HEIGHT/2-(button_h/2+5), button_w,
           button_h, 'MiniMax Algorithm', lambda: board_init("minimax"))
    Button(WIDTH/2-button_w/2, HEIGHT/2+(button_h/2+5), button_w,
           button_h, 'MCTS Algorithm', lambda: board_init("mcts"))
    while not game_running:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        for obj in objects:
            obj.process()
        pg.display.update()
        clock.tick(30)


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        font = pg.font.Font(None, 48)
        self.buttonSurface = pg.Surface((self.width, self.height))
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)

    def process(self):
        mousePos = pg.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                    objects.remove(self)
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
                    objects.remove(self)
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def main():
    pg.display.set_caption('Tic Tac Toe')
    menu()


if __name__ == '__main__':
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    objects = []
    main()
