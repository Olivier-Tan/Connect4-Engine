ROWS = 6
COLS = 7
WIN_CHECK_DIRECTIONS = [(0,1),(1,0),(1,1),(1,-1)]
WIN_CONDITION = 4

class Board:
    def __init__(self):
        self.grid = [[0 for col in range(COLS)] for row in range(ROWS)] 
        self.heights = [0] * COLS
        self.history = []

    # Returns which player's turn it is
    def player_turn(self):
        return len(self.history) % 2 + 1
    
    # Returns the columns that are able to have pieces placed in
    def legal_moves(self):
        legal = []
        for col in range(COLS):
            if self.heights[col] < ROWS:
                legal.append(col)
        return legal
    
    # Places piece into the board and updates relevant stats
    def place_piece(self, col):
        row = ROWS - 1 - self.heights[col]
        self.grid[row][col] = self.player_turn()
        self.heights[col] += 1
        self.history.append((row, col))
    
    # Undo the previous move 
    def undo(self):
        row, col = self.history.pop()
        self.grid[row][col] = 0
        self.heights[col] -= 1
    
    # Check if a player has won the game
    def check_win(self):
        if not self.history:
            return False
        row, col = self.history[-1]
        player = self.grid[row][col]
        for row_incr, col_incr in WIN_CHECK_DIRECTIONS:
            in_a_row = 1
            for sign in (1,-1):
                r = row + row_incr * sign
                c = col + col_incr * sign
                while 0 <= r < ROWS and 0 <= c < COLS and self.grid[r][c] == player:
                    in_a_row += 1
                    r += row_incr * sign
                    c += col_incr * sign
            if in_a_row >= WIN_CONDITION:
                return True
        return False
    
    # Check if the board has no more empty space
    def is_full(self):
        if len(self.history) >= ROWS * COLS:
            return True
        else:
            return False
    
    # Returns the winner of the game if won or 0 if tied or ongoing
    def winner(self):
        if self.check_win():
            row, col = self.history[-1]
            return self.grid[row][col]
        return 0

# Repeatedly asks for input until a valid input is made
def get_input(board):
    while True:
        player_input = input((f"Turn {len(board.history)}: Player {board.player_turn()} choose a column (1 - {COLS}) or 'q' to quit or 'u' to undo: "))

        if player_input in ('q', 'u'):
            if player_input == 'u' and not board.history:
                print("No previous moves available!")
                continue
            return player_input

        try:
            col = int(player_input) - 1
        except ValueError:
            print("Invalid input!")
            continue

        if col in board.legal_moves():
            return col

        print("Invalid input!")

def print_board(board):
    for row in range(ROWS):
        print(" ".join(str(cell) for cell in board.grid[row]))

# Main game loop
def main():
    board = Board()
    while True:
        print_board(board)
        
        player_input = get_input(board)
        
        if player_input == 'q':
            print(f"Exiting game")
            return

        if player_input == 'u':
            board.undo()
            continue
        
        board.place_piece(player_input)
        if board.is_full() or board.winner() != 0:
            print_board(board)
            winner = board.winner()
            if winner != 0: 
                print(f"Player {winner} wins!")
            else:
                print("Game tied!")
            return

if __name__ == "__main__":
    main()
