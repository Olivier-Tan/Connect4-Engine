from Benchmarks.benchmarks import make_board, measure, run
from Algorithms.minimax import minimax
from Algorithms.alpha_beta import alpha_beta


def test_benchmark_preserves_position(board):
    before = ([row[:] for row in board.grid], board.heights[:], board.history[:])
    result = measure(minimax, board, depth=2, repeats=2)
    assert result["nodes_evaluated"] > 0
    assert result["runtime_ms_median"] >= 0
    assert (board.grid, board.heights, board.history) == before


def test_benchmark_agrees_on_scores(board):
    rows = run(depths=[1, 2], repeats=1, fixtures={"early": [3, 2, 3]})
    assert len(rows) == 4
    for depth in (1, 2):
        values = [r["score"] for r in rows if r["depth"] == depth]
        assert len(set(values)) == 1


def test_benchmark_rejects_illegal_fixture(board):
    try:
        make_board([0, 0, 0, 0, 0, 0, 0])
        assert False, "Expected invalid fixture to fail"
    except ValueError:
        pass