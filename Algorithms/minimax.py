import math
import random
import time

from Algorithms.evaluation import evaluate_board, evaluate_position, evaluate_window


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
        best_col, value = None, evaluate_position(board, ai_player)
            
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