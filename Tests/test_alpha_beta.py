from Algorithms.alpha_beta import alpha_beta
from Algorithms.evaluation import WIN_SCORE, evaluate_board
from Algorithms.minimax import minimax
from Tests.helpers import play_moves, search


def test_alpha_beta_matches_minimax(board):
    for moves in ([], [3], [3, 2, 3, 4], [0, 6, 1, 6, 4, 5]):
        play_moves(board, moves)
        for ai_player in (1, 2):
            maximizing = board.player_turn() == ai_player
            expected = search(minimax, board, 3, maximizing, ai_player)
            col, score, _ = search(alpha_beta, board, 3, maximizing, ai_player)

            assert score == expected[1], f"Scores differ for {moves}, AI {ai_player}."
            assert col in board.legal_moves(), f"Expected a legal column, got {col}."
        while board.history:
            board.undo()


def test_alpha_beta_empty_board(board):
    col, _, _ = search(alpha_beta, board, 2, True, 1)

    assert col in board.legal_moves(), "Expected a legal opening move."


def test_alpha_beta_win(board):
    play_moves(board, [0, 6, 1, 6, 2, 5])

    col, score, _ = search(alpha_beta, board, 2, True, 1)

    assert col == 3, f"Expected winning column 3, got {col}."
    assert score == WIN_SCORE, f"Expected winning score, got {score}."


def test_alpha_beta_opponent_win(board):
    play_moves(board, [0, 6, 1, 6, 4, 6, 4])

    col, score, _ = search(alpha_beta, board, 1, False, 1)

    assert col == 6, f"Expected opponent's winning column 6, got {col}."
    assert score == -WIN_SCORE, f"Expected losing score for the AI, got {score}."


def test_alpha_beta_blocks_opponent_win(board):
    play_moves(board, [0, 6, 1, 6, 4, 6])

    col, _, _ = search(alpha_beta, board, 2, True, 1)

    assert col == 6, f"Expected blocking column 6, got {col}."


def test_alpha_beta_finished_ai_win(board):
    play_moves(board, [6, 0, 6, 1, 5, 2, 5, 3])
    assert board.winner() == 2, "Expected Player 2 to have already won."

    col, score, stats = search(alpha_beta, board, 2, False, 2)

    assert col is None, "An already won game should not select a move."
    assert score == WIN_SCORE, f"Expected winning score for Player 2, got {score}."
    assert stats["nodes_evaluated"] == 1, "Search should stop at the terminal root."


def test_alpha_beta_finished_opponent_win(board):
    play_moves(board, [0, 6, 1, 6, 2, 5, 3])
    assert board.winner() == 1, "Expected Player 1 to have already won."

    col, score, stats = search(alpha_beta, board, 2, True, 2)

    assert col is None, "An already lost game should not select a move."
    assert score == -WIN_SCORE, f"Expected losing score for Player 2, got {score}."
    assert stats["nodes_evaluated"] == 1, "Search should stop at the terminal root."


def test_alpha_beta_full_board_draw(board):
    play_moves(board, [
        0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0,
        2, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2,
        4, 5, 4, 5, 4, 5, 5, 4, 5, 4, 5, 4,
        6, 6, 6, 6, 6, 6,
    ])
    assert board.is_full() and board.winner() == 0, "Expected a full board draw."

    col, score, stats = search(alpha_beta, board, 2, True, 1)

    assert col is None, "A full board should not select a move."
    assert score == 0, f"Expected draw score 0, got {score}."
    assert stats["nodes_evaluated"] == 1, "Search should stop at the terminal root."


def test_alpha_beta_depth_zero(board):
    play_moves(board, [3, 0])
    expected_score = evaluate_board(board, 1)

    col, score, stats = search(alpha_beta, board, 0, True, 1)

    assert col is None, "Depth zero should not select a move."
    assert score == expected_score, "Expected evaluation of the current board."
    assert stats["nodes_evaluated"] == 1, "Depth zero should visit only the root."


def test_alpha_beta_full_column(board):
    play_moves(board, [3, 3, 3, 3, 3, 3])
    assert 3 not in board.legal_moves(), "Expected column 3 to be full."

    col, _, _ = search(alpha_beta, board, 2, True, 1)

    assert col in board.legal_moves(), f"Expected a legal column, got {col}."
    assert col != 3, "Search selected the full column."


def test_alpha_beta_prunes_nodes(board):
    _, expected_score, minimax_stats = search(minimax, board, 4, True, 1)
    _, score, stats = search(alpha_beta, board, 4, True, 1)

    assert score == expected_score, "Pruning changed the minimax score."
    assert stats["nodes_evaluated"] < minimax_stats["nodes_evaluated"], "Expected fewer searched nodes."
    assert set(stats) == {"nodes_evaluated", "time_seconds", "nodes_per_second"}, "Unexpected statistics keys."
    assert stats["time_seconds"] >= 0 and stats["nodes_per_second"] >= 0, "Expected nonnegative timing statistics."


def test_alpha_beta_supplied_stats(board):
    play_moves(board, [3, 2])
    stats = {"nodes_evaluated": 0, "start_time": 0.0}
    expected = search(minimax, board, 2, True, 1)

    result = search(lambda *args: alpha_beta(*args, stats=stats), board, 2, True, 1)

    assert len(result) == 2, "A call with supplied statistics should return a pair."
    assert result[1] == expected[1], "Expected the minimax score with supplied statistics."
    assert stats["nodes_evaluated"] > 1, "Expected the shared node counter to be updated."
    assert set(stats) == {"nodes_evaluated", "start_time"}, "A recursive call should not finalize statistics."
