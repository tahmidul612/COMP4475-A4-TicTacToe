class MiniMax:
    """MiniMax algorithm
    """    
    def __init__(self, board: list[list[None]], ai):
        self.board = board
        self.ai = ai
        self.human = 'x' if ai == 'o' else 'o'
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

    def no_moves(self, board):
        return all([cell != None for row in board for cell in row])

    def minimax(self, board, depth, isMaximizing):      
        """
        Applies the minimax algorithm to determine the best move for the AI player.

        Args:
            board: The current state of the tic-tac-toe board.
            depth: The current depth of the minimax search.
            isMaximizing: A boolean indicating whether it is the AI player's turn or not.

        Returns:
            The score of the best move for the AI player.

        """
        score = self.check_win(board)
        if (score in [-10, 10]):
            return score
        elif self.no_moves(board):
            return 0
        if isMaximizing:
            max_score = -1000
            for row in range(3):
                for col in range(3):
                    if board[row][col] == None:
                        board[row][col] = self.ai
                        max_score = max(max_score, self.minimax(
                            board, depth+1, not isMaximizing))
                        board[row][col] = None
            return max_score
        else:
            min_score = 1000
            for row in range(3):
                for col in range(3):
                    if board[row][col] == None:
                        board[row][col] = self.human
                        min_score = min(min_score, self.minimax(
                            board, depth+1, not isMaximizing))
                        board[row][col] = None
            return min_score

    def best_move(self, board):
        best_score = -1000
        best_move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if board[row][col] == None:
                    board[row][col] = self.ai
                    score = self.minimax(board, 0, False)
                    board[row][col] = None
                    print(f'{row}, {col} = {score}')
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        print(
            f'MiniMax best move: row - {best_move[0]}, col - {best_move[1]} || Score : {best_score}')
        return best_move
