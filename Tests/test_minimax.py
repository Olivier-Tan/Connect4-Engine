from Algorithms.evaluation import WIN_SCORE, evaluate_board
from Algorithms.minimax import minimax
from Tests.helpers import play_moves, search


def test_minimax_empty_board(board):
    col, _, _ = search(minimax, board, 2, True, 1)

    assert col in board.legal_moves(), "Expected a legal opening move."


def test_minimax_win(board):
    play_moves(board, [0, 6, 1, 6, 2, 5])

    col, score, _ = search(minimax, board, 2, True, 1)

    assert col == 3, f"Expected winning column 3, got {col}."
    assert score == WIN_SCORE, f"Expected winning score, got {score}."


def test_minimax_opponent_win(board):
    play_moves(board, [0, 6, 1, 6, 4, 6, 4])

    col, score, _ = search(minimax, board, 1, False, 1)

    assert col == 6, f"Expected opponent's winning column 6, got {col}."
    assert score == -WIN_SCORE, f"Expected losing score for the AI, got {score}."


def test_minimax_blocks_opponent_win(board):
    play_moves(board, [0, 6, 1, 6, 4, 6])

    col, _, _ = search(minimax, board, 2, True, 1)

    assert col == 6, f"Expected blocking column 6, got {col}."


def test_minimax_full_board_draw(board):
    play_moves(board, [
        0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0,
        2, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2,
        4, 5, 4, 5, 4, 5, 5, 4, 5, 4, 5, 4,
        6, 6, 6, 6, 6, 6,
    ])
    assert board.is_full() and board.winner() == 0, "Expected a full board draw."

    col, score, stats = search(minimax, board, 2, True, 1)

    assert col is None, "A full board should not select a move."
    assert score == 0, f"Expected draw score 0, got {score}."
    assert stats["nodes_evaluated"] == 1, "Search should stop at the terminal root."


def test_minimax_finished_ai_win(board):
    play_moves(board, [6, 0, 6, 1, 5, 2, 5, 3])
    assert board.winner() == 2, "Expected Player 2 to have already won."

    col, score, stats = search(minimax, board, 2, False, 2)

    assert col is None, "An already won game should not select a move."
    assert score == WIN_SCORE, f"Expected winning score for Player 2, got {score}."
    assert stats["nodes_evaluated"] == 1, "Search should stop at the terminal root."


def test_minimax_finished_opponent_win(board):
    play_moves(board, [0, 6, 1, 6, 2, 5, 3])
    assert board.winner() == 1, "Expected Player 1 to have already won."

    col, score, stats = search(minimax, board, 2, True, 2)

    assert col is None, "An already lost game should not select a move."
    assert score == -WIN_SCORE, f"Expected losing score for Player 2, got {score}."
    assert stats["nodes_evaluated"] == 1, "Search should stop at the terminal root."


def test_minimax_depth_zero(board):
    play_moves(board, [3, 0])
    expected_score = evaluate_board(board, 1)

    col, score, stats = search(minimax, board, 0, True, 1)

    assert col is None, "Depth zero should not select a move."
    assert score == expected_score, "Expected evaluation of the current board."
    assert stats["nodes_evaluated"] == 1, "Depth zero should visit only the root."


def test_minimax_full_column(board):
    play_moves(board, [3, 3, 3, 3, 3, 3])
    assert 3 not in board.legal_moves(), "Expected column 3 to be full."

    col, _, _ = search(minimax, board, 2, True, 1)

    assert col in board.legal_moves(), f"Expected a legal column, got {col}."
    assert col != 3, "Search selected the full column."
