import tkinter as tk
import queue
import random

# Constants for the game
EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"

# Initialize the game board
def initialize_board():
    return [[EMPTY] * 3 for _ in range(3)]

# Check for a winner
def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # Row check
            return True
        if all(board[j][i] == player for j in range(3)):  # Column check
            return True
    if all(board[i][i] == player for i in range(3)):  # Diagonal check
        return True
    if all(board[i][2 - i] == player for i in range(3)):  # Anti-diagonal check
        return True
    return False

# Check if the board is full
def is_board_full(board):
    return all(board[i][j] != EMPTY for i in range(3) for j in range(3))

# Get available moves
def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

# BFS Algorithm
def bfs(board, player):
    q = queue.Queue()
    q.put((board, player))
    while not q.empty():
        current_board, current_player = q.get()
        available_moves = get_available_moves(current_board)
        for move in available_moves:
            i, j = move
            new_board = [row.copy() for row in current_board]
            new_board[i][j] = current_player
            if check_winner(new_board, current_player):
                return move
            next_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
            q.put((new_board, next_player))
    return random.choice(get_available_moves(board))



def dfs(self):
        """AI move using Depth-First Search."""
        stack = [(self.board, None)]
        while stack:
            state, move = stack.pop()
            for i in range(9):
                if state[i] == ' ':
                    new_state = state[:]
                    new_state[i] = 'O'
                    if self.check_winner_simulated(new_state, 'O'):
                        return i
                    stack.append((new_state, i))
        return self.find_first_empty()


# UCS Algorithm (simplified for Tic-Tac-Toe)
def ucs(board, player):
    q = queue.PriorityQueue()
    q.put((0, board, player))
    while not q.empty():
        cost, current_board, current_player = q.get()
        available_moves = get_available_moves(current_board)
        for move in available_moves:
            i, j = move
            new_board = [row.copy() for row in current_board]
            new_board[i][j] = current_player
            if check_winner(new_board, current_player):
                return move
            next_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
            q.put((cost + 1, new_board, next_player))
    return random.choice(get_available_moves(board))

# GUI Setup with Tkinter
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = initialize_board()
        self.current_player = PLAYER_X
        self.game_mode = "1"
        self.algorithm = "bfs"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.create_widgets()
        
    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text=EMPTY, width=10, height=3, font=("Arial", 20),
                                               command=lambda i=i, j=j: self.on_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)
        
        self.mode_label = tk.Label(self.root, text="Choose Mode:")
        self.mode_label.grid(row=3, column=0)
        
        self.mode_var = tk.StringVar(value="1")
        self.one_player_radio = tk.Radiobutton(self.root, text="1 Player", variable=self.mode_var, value="1", command=self.set_game_mode)
        self.one_player_radio.grid(row=3, column=1)
        self.two_player_radio = tk.Radiobutton(self.root, text="2 Player", variable=self.mode_var, value="2", command=self.set_game_mode)
        self.two_player_radio.grid(row=3, column=2)

        self.algorithm_label = tk.Label(self.root, text="Choose Algorithm:")
        self.algorithm_label.grid(row=4, column=0)
        
        self.algorithm_var = tk.StringVar(value="bfs")
        self.bfs_radio = tk.Radiobutton(self.root, text="BFS", variable=self.algorithm_var, value="bfs")
        self.bfs_radio.grid(row=4, column=1)
        self.dfs_radio = tk.Radiobutton(self.root, text="DFS", variable=self.algorithm_var, value="dfs")
        self.dfs_radio.grid(row=4, column=2)
        self.ucs_radio = tk.Radiobutton(self.root, text="UCS", variable=self.algorithm_var, value="ucs")
        self.ucs_radio.grid(row=4, column=3)
        
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=5, column=0, columnspan=3)
    
    def set_game_mode(self):
        self.game_mode = self.mode_var.get()
        self.algorithm = self.algorithm_var.get()

    def on_click(self, i, j):
        if not self.game_over and self.board[i][j] == EMPTY:
            make_move(self.board, i, j, self.current_player)
            self.buttons[i][j].config(text=self.current_player)
            if check_winner(self.board, self.current_player):
                self.display_winner(self.current_player)
                return
            if is_board_full(self.board):
                self.display_draw()
                return
            
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

            if self.game_mode == "1" and self.current_player == PLAYER_O:
                self.root.after(500, self.play_ai)  # Add delay for AI move

    def play_ai(self):
        algorithm_func = {"bfs": bfs, "dfs": dfs, "ucs": ucs}[self.algorithm]
        move = algorithm_func(self.board, PLAYER_O)
        i, j = move
        make_move(self.board, i, j, PLAYER_O)
        self.buttons[i][j].config(text=PLAYER_O)
        if check_winner(self.board, PLAYER_O):
            self.display_winner(PLAYER_O)
        elif is_board_full(self.board):
            self.display_draw()
        else:
            self.current_player = PLAYER_X

    def display_winner(self, player):
        self.game_over = True
        tk.Label(self.root, text=f"Player {player} wins!", font=("Arial", 16)).grid(row=6, column=0, columnspan=3)
        self.disable_buttons()

    def display_draw(self):
        self.game_over = True
        tk.Label(self.root, text="It's a draw!", font=("Arial", 16)).grid(row=6, column=0, columnspan=3)
        self.disable_buttons()

    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")

    def reset_game(self):
        self.board = initialize_board()
        self.current_player = PLAYER_X
        self.game_over = False
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=EMPTY, state="normal")

def make_move(board, i, j, player):
    board[i][j] = player

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
