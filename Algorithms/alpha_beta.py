import math
import random
import time

from Algorithms.evaluation import evaluate_position


def alpha_beta(
    board,
    depth,
    is_maximizing,
    ai_player,
    stats=None,
    alpha=-math.inf,
    beta=math.inf,
):
    is_root = False
    if stats is None:
        is_root = True
        stats = {
            "nodes_evaluated": 0,
            "start_time": time.perf_counter()
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
            new_score = alpha_beta(board, depth - 1, False, ai_player, stats, alpha, beta)[1]
            board.undo()

            if new_score > value:
                value = new_score
                best_col = col

            # Update alpha and conditionally prone
            alpha = max(alpha, value)
            if alpha >= beta:
                break

    # RECURSIVE STEP: Minimizing Player (The Opponent)
    else:
        value = math.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            board.place_piece(col)
            new_score = alpha_beta(board, depth - 1, True, ai_player, stats, alpha, beta)[1]
            board.undo()

            if new_score < value:
                value = new_score
                best_col = col

            # Update beta and conditionally prone
            beta = min(beta, value)
            if alpha >= beta:
                break

    if is_root:
        elapsed = time.perf_counter() - stats["start_time"]
        stats["time_seconds"] = elapsed
        stats["nodes_per_second"] = stats["nodes_evaluated"] / elapsed if elapsed > 0 else 0
        del stats["start_time"]
        return best_col, value, stats
    else:
        return best_col, value
