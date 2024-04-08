class MiniMax():
    def __init__(self, board: list[list[None]], ai, human):
        self.board = board.copy()
        self.ai = ai
        self.human = human
        global winner, draw
        winner, draw = None, False


    def check_win(self, board):
        global winner, draw
        # Check for win in rows
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] and board[row][0] != None:
                if board[row][0] == self.ai:
                    return 10
                elif board[row][0] == self.human:
                    return -10
        # Check for win in columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != None:
                if board[0][col] == self.ai:
                    return 10
                elif board[0][col] == self.human:
                    return -10
        # Check for win in diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != None:
            winner = board[0][0]
            if board[0][0] == self.ai:
                return 10
            elif board[0][0] == self.human:
                return -10
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != None:
            if board[0][2] == self.ai:
                return 10
            elif board[0][2] == self.human:
                return -10
        return 0
    
    def noMoves(self, board):
        global winner, draw
        return all([cell != None for row in board for cell in row]) and winner == None
    
    def minimax(self, board, depth, isMaximizing):
        score = self.check_win(board)
        if (score in [-10, 10]):
            return score
        elif self.noMoves(board):
            return 0
        if isMaximizing:
            max_score = -1000
            for row in range(3):
                for col in range(3):
                    if board[row][col] == None:
                        board[row][col] = self.ai
                        max_score = max(max_score, self.minimax(board, depth+1, not isMaximizing))
                        board[row][col] = None
            return max_score
        else:
            min_score = 1000
            for row in range(3):
                for col in range(3):
                    if board[row][col] == None:
                        board[row][col] = self.human
                        min_score = min(min_score, self.minimax(board, depth+1, not isMaximizing))
                        board[row][col] = None
            return min_score
    def bestMove(self, board):
        best_score = -1000
        best_move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if board[row][col] == None:
                    board[row][col] = self.ai
                    score = self.minimax(board, 0, False)
                    board[row][col] = None
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        print(f'MiniMax best move: row - {best_move[0]}, col - {best_move[1]} || Score : {best_score}')
        return best_move