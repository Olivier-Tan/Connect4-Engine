import math
import time

from Algorithms.evaluation import evaluate_position
from Algorithms.move_ordering import order_moves


def alpha_beta_ordered(
    board,
    depth,
    is_maximizing,
    ai_player,
    strategy,
    stats=None,
    alpha=-math.inf,
    beta=math.inf,
):
    is_root = False

    if stats is None:
        is_root = True

        stats = {
            "nodes_evaluated": 0,
            "cutoffs": 0,
            "start_time": time.perf_counter()
        }

    stats["nodes_evaluated"] += 1

    is_terminal = board.check_win() or board.is_full()

    # BASE CASE
    if depth == 0 or is_terminal:
        best_col = None
        value = evaluate_position(board, ai_player)

    else:
        # The important difference from normal alpha-beta
        valid_moves = order_moves(
            board,
            ai_player,
            is_maximizing,
            strategy
        )

        # MAXIMIZING PLAYER
        if is_maximizing:
            value = -math.inf
            best_col = valid_moves[0]

            for col in valid_moves:
                board.place_piece(col)

                new_score = alpha_beta_ordered(
                    board,
                    depth - 1,
                    False,
                    ai_player,
                    strategy,
                    stats,
                    alpha,
                    beta
                )[1]

                board.undo()

                if new_score > value:
                    value = new_score
                    best_col = col

                alpha = max(alpha, value)

                if alpha >= beta:
                    stats["cutoffs"] += 1
                    break

        # MINIMIZING PLAYER
        else:
            value = math.inf
            best_col = valid_moves[0]

            for col in valid_moves:
                board.place_piece(col)

                new_score = alpha_beta_ordered(
                    board,
                    depth - 1,
                    True,
                    ai_player,
                    strategy,
                    stats,
                    alpha,
                    beta
                )[1]

                board.undo()

                if new_score < value:
                    value = new_score
                    best_col = col

                beta = min(beta, value)

                if alpha >= beta:
                    stats["cutoffs"] += 1
                    break

    if is_root:
        elapsed = time.perf_counter() - stats["start_time"]

        stats["time_seconds"] = elapsed

        stats["nodes_per_second"] = (
            stats["nodes_evaluated"] / elapsed
            if elapsed > 0
            else 0
        )

        del stats["start_time"]

        return best_col, value, stats

    return best_col, value