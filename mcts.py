import math
import random


class MCTS:
    """Monte Carlo Tree Search algorithm
    """

    def __init__(self, board, player, iterations=1000):
        self.board = board
        self.player = player
        self.iterations = iterations

    def best_move(self, board):
        """
        Finds the best move to play on the given board using the Monte Carlo Tree Search algorithm.

        Args:
            board (list): The current state of the game board.

        Returns:
            tuple: The best move to play on the board.

        """
        root = Node(Board(board, self.player))
        for _ in range(self.iterations):
            node = root
            game_state = root.game_state.copy()

            # Selection
            node = self._selection(node, game_state)

            # Expansion
            if node.untried_moves:
                node = self._expansion(node, game_state)

            # Backpropagation
            self._backpropagate(node, game_state)

        # return the move that was most visited
        return max(root.children, key=lambda c: c.visits).move

    def _selection(self, node, game_state):
        while node.untried_moves == [] and node.children != []:  # node is fully expanded and non-terminal
            node = node.select_child()
            game_state.make_move(*node.move)
        return node

    def _expansion(self, node, game_state):
        game_state_copy = game_state.copy()
        while node.untried_moves != []:
            move = random.choice(node.untried_moves)
            # add child and descend tree
            node = node.add_child(move, game_state)
            game_state = self._simulation(game_state_copy)
        return node

    def _simulation(self, game_state):
        while game_state.empty:  # while state is non-terminal
            game_state.make_move(*random.choice(game_state.empty))
        return game_state

    def _backpropagate(self, node, game_state):
        while node:  # backpropagate from the expanded node and work back to the root node
            # Update node with result from POV of the player who made the last move
            result = (0, 0, 0)
            if game_state.check_win(node.game_state.current_player) == 10:
                result = (1, 0, 0)
            elif game_state.check_win(node.game_state.current_player) == -10:
                result = (0, 1, 0)
            elif game_state.check_win(node.game_state.current_player) == 0:
                result = (0, 0, 1)
            node.update(*result)
            node = node.parent


class Board:
    """Utility class to represent the game board and game state
    """

    def __init__(self, board, player='x'):
        self.board = board
        self.empty = [(x, y) for x in range(3)
                      for y in range(3) if board[x][y] is None]
        self.player = player
        self.current_player = player

    def check_win(self, ai):
        human = 'x' if ai == 'o' else 'o'
        # Check for win in rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] != None:
                if self.board[row][0] == ai:
                    return 10
                elif self.board[row][0] == human:
                    return -10
        # Check for win in columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != None:
                if self.board[0][col] == ai:
                    return 10
                elif self.board[0][col] == human:
                    return -10
        # Check for win in diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != None:
            if self.board[0][0] == ai:
                return 10
            elif self.board[0][0] == human:
                return -10
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != None:
            if self.board[0][2] == ai:
                return 10
            elif self.board[0][2] == human:
                return -10
        if all([cell != None for row in self.board for cell in row]):
            return 0
        return float('-inf')

    def is_draw(self):
        return len(self.empty) == 0

    def make_move(self, x, y):
        if (x, y) in self.empty:
            self.board[x][y] = self.current_player
            self.empty.remove((x, y))
            self.current_player = 'o' if self.current_player == 'x' else 'x'
            return True
        return False

    def copy(self):
        return Board([row[:] for row in self.board], self.player)


class Node:
    """Node class for MCTS
    """

    def __init__(self, game_state: Board, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.visits = 0
        self.children = []
        self.untried_moves = game_state.empty

    def UCB1(self, total_simulations, c_param=1.41):
        """Calculate UCB1 score for the node"""
        if self.visits == 0:
            return float('inf')  # Avoid division by zero
        return self.value() + c_param * math.sqrt(math.log(total_simulations) / self.visits)

    def select_child(self):
        """ Select a child node with highest UCB1 score """
        return max(self.children, key=lambda x: x.UCB1(self.visits))

    def add_child(self, move, game_state):
        child = Node(game_state=game_state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, win, loss, draw):
        self.visits += 1
        self.wins += win
        self.losses += loss
        self.draws += draw

    def value(self):
        if self.visits == 0:
            return 0
        return (self.wins+self.draws)-self.losses / self.visits
