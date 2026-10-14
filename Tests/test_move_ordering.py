from Algorithms.evaluation import evaluate_position
from Algorithms.move_ordering import (
    center_first,
    heuristic_order,
    order_moves,
)
from Tests.helpers import play_moves


def test_center_first_empty_board(board):
    moves = center_first(board)

    assert moves == [3, 2, 4, 1, 5, 0, 6], (
        f"Expected centre-first ordering, got {moves}."
    )


def test_center_first_only_returns_legal_moves(board):
    # Fill column 3 completely.
    play_moves(board, [3, 3, 3, 3, 3, 3])

    assert 3 not in board.legal_moves(), "Expected column 3 to be full."

    moves = center_first(board)

    assert 3 not in moves, "Centre-first ordering included a full column."
    assert set(moves) == set(board.legal_moves()), (
        "Centre-first ordering should contain exactly the legal moves."
    )


def test_center_first_order_with_full_columns(board):
    # Fill the centre column and column 2.
    play_moves(board, [3, 3, 3, 3, 3, 3])
    play_moves(board, [2, 2, 2, 2, 2, 2])

    moves = center_first(board)

    expected = [4, 1, 5, 0, 6]

    assert moves == expected, (
        f"Expected {expected}, got {moves}."
    )


def test_center_first_does_not_modify_board(board):
    play_moves(board, [3, 2, 4, 1])

    original_grid = [row[:] for row in board.grid]
    original_heights = board.heights[:]
    original_history = board.history[:]

    center_first(board)

    assert board.grid == original_grid, (
        "Centre-first ordering modified the board grid."
    )
    assert board.heights == original_heights, (
        "Centre-first ordering modified column heights."
    )
    assert board.history == original_history, (
        "Centre-first ordering modified move history."
    )


def test_heuristic_order_returns_all_legal_moves(board):
    play_moves(board, [3, 2, 3, 4])

    moves = heuristic_order(
        board,
        ai_player=1,
        is_maximizing=True,
    )

    assert set(moves) == set(board.legal_moves()), (
        "Heuristic ordering should contain exactly the legal moves."
    )

    assert len(moves) == len(board.legal_moves()), (
        "Heuristic ordering returned the wrong number of moves."
    )


def test_heuristic_order_maximizing(board):
    play_moves(board, [0, 6, 1, 6])

    legal_moves = board.legal_moves()

    # Work out the expected score of every move.
    scored_moves = []

    for col in legal_moves:
        board.place_piece(col)
        score = evaluate_position(board, 1)
        board.undo()

        scored_moves.append((score, col))

    expected = [
        col
        for score, col in sorted(
            scored_moves,
            key=lambda item: item[0],
            reverse=True,
        )
    ]

    moves = heuristic_order(
        board,
        ai_player=1,
        is_maximizing=True,
    )

    assert moves == expected, (
        f"Expected maximizing order {expected}, got {moves}."
    )


def test_heuristic_order_minimizing(board):
    play_moves(board, [0, 6, 1, 6])

    legal_moves = board.legal_moves()

    scored_moves = []

    for col in legal_moves:
        board.place_piece(col)
        score = evaluate_position(board, 1)
        board.undo()

        scored_moves.append((score, col))

    expected = [
        col
        for score, col in sorted(
            scored_moves,
            key=lambda item: item[0],
        )
    ]

    moves = heuristic_order(
        board,
        ai_player=1,
        is_maximizing=False,
    )

    assert moves == expected, (
        f"Expected minimizing order {expected}, got {moves}."
    )


def test_heuristic_order_does_not_modify_board(board):
    play_moves(board, [3, 2, 3, 4])

    original_grid = [row[:] for row in board.grid]
    original_heights = board.heights[:]
    original_history = board.history[:]

    heuristic_order(
        board,
        ai_player=1,
        is_maximizing=True,
    )

    assert board.grid == original_grid, (
        "Heuristic ordering modified the board grid."
    )
    assert board.heights == original_heights, (
        "Heuristic ordering modified column heights."
    )
    assert board.history == original_history, (
        "Heuristic ordering modified move history."
    )


def test_heuristic_order_full_column(board):
    play_moves(board, [3, 3, 3, 3, 3, 3])

    assert 3 not in board.legal_moves(), (
        "Expected column 3 to be full."
    )

    moves = heuristic_order(
        board,
        ai_player=1,
        is_maximizing=True,
    )

    assert 3 not in moves, (
        "Heuristic ordering included a full column."
    )


def test_order_moves_center_strategy(board):
    moves = order_moves(
        board,
        ai_player=1,
        is_maximizing=True,
        strategy="center",
    )

    assert moves == [3, 2, 4, 1, 5, 0, 6], (
        f"Expected centre-first ordering, got {moves}."
    )


def test_order_moves_heuristic_strategy(board):
    play_moves(board, [3, 2, 3, 4])

    expected = heuristic_order(
        board,
        ai_player=1,
        is_maximizing=True,
    )

    moves = order_moves(
        board,
        ai_player=1,
        is_maximizing=True,
        strategy="heuristic",
    )

    assert moves == expected, (
        "order_moves did not use heuristic ordering correctly."
    )


def test_order_moves_invalid_strategy(board):
    try:
        order_moves(
            board,
            ai_player=1,
            is_maximizing=True,
            strategy="invalid",
        )

        assert False, "Expected invalid strategy to raise ValueError."

    except ValueError:
        pass