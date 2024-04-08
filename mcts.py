import math,random

class Board:
    def __init__(self, board):
        self.board = board
        self.empty = [(x, y) for x in range(3)
                      for y in range(3) if board[x][y] is None]
        self.current_player = 'X'

    def is_win(self, player):
        # Check if player wins in any row or column
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or all(self.board[j][i] == player for j in range(3)):
                return True
        # Check if player wins in any diagonal
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return len(self.empty) == 0

    def make_move(self, x, y):
        if (x, y) in self.empty:
            self.board[x][y] = self.current_player
            self.empty.remove((x, y))
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def copy(self):
        return Board([row[:] for row in self.board])


class Node:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.untried_moves = game_state.empty

    def UCB1(self, total_simulations, c_param=1.41):
        if self.visits == 0:
            return float('inf')  # Avoid division by zero
        return self.wins / self.visits + c_param * (2 * math.log(total_simulations) / self.visits)**0.5

    def select_child(self):
        # Select a child node with highest UCB1 score
        return sorted(self.children, key=lambda x: x.UCB1(self.visits))[0]

    def add_child(self, move, game_state):
        child = Node(game_state=game_state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

class MCTS:
    def __init__(self, board, player, iterations=1000):
        self.root = Node(Board(board))
        self.player = player
        self.iterations = iterations
        
    def best_move(self,board):
        root = Node(Board(board))
        for _ in range(self.iterations):
            node = root
            game_state = root.game_state.copy()

            # Selection
            while node.untried_moves == [] and node.children != []:  # node is fully expanded and non-terminal
                node = node.select_child()
                game_state.make_move(*node.move)

            # Expansion
            # if we can expand (i.e. state/node is non-terminal)
            if node.untried_moves:
                m = random.choice(node.untried_moves)
                game_state.make_move(*m)
                node = node.add_child(m, game_state)  # add child and descend tree

            # Simulation
            while game_state.empty:  # while state is non-terminal
                game_state.make_move(*random.choice(game_state.empty))

            # Backpropagation
            while node:  # backpropagate from the expanded node and work back to the root node
                # Update node with result from POV of node.playerJustMoved
                node.update(1 if game_state.is_win(
                    node.game_state.current_player) else 0)
                node = node.parent

        # return the move that was most visited
        return sorted(root.children, key=lambda c: c.visits)[-1].move
