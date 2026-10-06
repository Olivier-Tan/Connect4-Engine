import math
import random

ROWS = 6
COLS = 7

def evaluate_window(window, piece):
    """Scores a slice of 4 slots to help the AI gauge if a move is good."""
    score = 0
    opp_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # Block opponent's 3-in-a-row
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def evaluate_board(board, piece):
    """Scans the whole board and tallies up the score for a specific player."""
    score = 0
    
    # Priority 1: Control the center column
    center_array = [int(board.grid[r][COLS//2]) for r in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROWS):
        row_array = board.grid[r]
        for c in range(COLS-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLS):
        col_array = [board.grid[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score Positive Diagonal
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board.grid[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score Negative Diagonal
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board.grid[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def minimax(board, depth, is_maximizing, ai_player):
    """The recursive algorithm that plays out future scenarios."""
    valid_moves = board.legal_moves()
    is_terminal = board.check_win() or board.is_full()
    
    # BASE CASE
    if depth == 0 or is_terminal:
        if is_terminal:
            if board.winner() == ai_player:
                return (None, 1000000) # AI wins
            elif board.winner() != 0:
                return (None, -1000000) # Opponent wins
            else:
                return (None, 0) # Draw
        else:
            return (None, evaluate_board(board, ai_player))
            
    # RECURSIVE STEP: Maximizing Player (The AI)
    if is_maximizing:
        value = -math.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            board.place_piece(col)
            new_score = minimax(board, depth - 1, False, ai_player)[1]
            board.undo()
            
            if new_score > value:
                value = new_score
                best_col = col
        return best_col, value
        
    # RECURSIVE STEP: Minimizing Player (The Opponent)
    else: 
        value = math.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            board.place_piece(col)
            new_score = minimax(board, depth - 1, True, ai_player)[1]
            board.undo()
            
            if new_score < value:
                value = new_score
                best_col = col
        return best_col, value