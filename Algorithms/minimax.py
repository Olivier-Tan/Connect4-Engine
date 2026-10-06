import math
import random
import time

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

def minimax(board, depth, is_maximizing, ai_player, stats=None):
    """The recursive algorithm that plays out future scenarios."""
    
    # 1. Root level setup: If stats is None, this is the very first call from main.py
    is_root = False
    if stats is None:
        is_root = True
        stats = {
            "nodes_evaluated": 0,
            "start_time": time.perf_counter() # Highest available timer resolution
        }
        
    stats["nodes_evaluated"] += 1

    valid_moves = board.legal_moves()
    is_terminal = board.check_win() or board.is_full()
    
    # BASE CASE
    if depth == 0 or is_terminal:
        if is_terminal:
            if board.winner() == ai_player:
                best_col, value = None, 1000000 # AI wins
            elif board.winner() != 0:
                best_col, value = None, -1000000 # Opponent wins
            else:
                best_col, value = None, 0 # Draw
        else:
            best_col, value = None, evaluate_board(board, ai_player)
            
    # RECURSIVE STEP: Maximizing Player (The AI)
    elif is_maximizing:
        value = -math.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            board.place_piece(col)
            # Pass stats down; child nodes will know they are not the root
            new_score = minimax(board, depth - 1, False, ai_player, stats)[1]
            board.undo()
            
            if new_score > value:
                value = new_score
                best_col = col
        
    # RECURSIVE STEP: Minimizing Player (The Opponent)
    else: 
        value = math.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            board.place_piece(col)
            # Pass stats down; child nodes will know they are not the root
            new_score = minimax(board, depth - 1, True, ai_player, stats)[1]
            board.undo()
            
            if new_score < value:
                value = new_score
                best_col = col
                
    # 2. Return logic: Finalize stats at the root, otherwise return standard tuple
    if is_root:
        elapsed = time.perf_counter() - stats["start_time"]
        stats["time_seconds"] = elapsed
        stats["nodes_per_second"] = stats["nodes_evaluated"] / elapsed if elapsed > 0 else 0
        del stats["start_time"] # Clean up internal tracking data
        return best_col, value, stats
    else:
        return best_col, value