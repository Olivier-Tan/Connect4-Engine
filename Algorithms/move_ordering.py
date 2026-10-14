from Algorithms.evaluation import evaluate_position


CENTER_ORDER = [3, 2, 4, 1, 5, 0, 6]


def center_first(board):
    """
    Returns legal moves with centre columns searched first.
    """
    legal_moves = set(board.legal_moves())

    return [
        col
        for col in CENTER_ORDER
        if col in legal_moves
    ]


def heuristic_order(board, ai_player, is_maximizing):
    """
    Orders legal moves using the board evaluation function.

    Maximizing:
        highest score first

    Minimizing:
        lowest score first
    """
    scored_moves = []

    for col in board.legal_moves():
        board.place_piece(col)

        score = evaluate_position(board, ai_player)

        board.undo()

        scored_moves.append((score, col))

    scored_moves.sort(
        key=lambda item: item[0],
        reverse=is_maximizing
    )

    return [col for score, col in scored_moves]


def order_moves(board, ai_player, is_maximizing, strategy):
    """
    Returns legal moves according to the selected strategy.
    """

    if strategy == "center":
        return center_first(board)

    elif strategy == "heuristic":
        return heuristic_order(
            board,
            ai_player,
            is_maximizing
        )

    else:
        raise ValueError(
            f"Unknown move ordering strategy: {strategy}"
        )