import random
from Benchmarks.generate_boards import RANGES, generate_board, generate_dataset, replay


def test_generator_categories(board):
    for i, (category, (low, high)) in enumerate(RANGES.items()):
        generated, moves = generate_board(category, random.Random(3821 + i))
        assert low <= len(moves) <= high
        assert not generated.check_win() and not generated.is_full()
        assert len(generated.history) == len(moves)
        assert replay(moves).grid == generated.grid


def test_generator_boundaries(board):
    for category, target in (("early", 0), ("early", 13), ("mid", 14), ("late", 27), ("late", 30)):
        generated, moves = generate_board(category, random.Random(1234), target_moves=target)
        assert len(moves) == target
        assert not generated.check_win()
        assert replay(moves).heights == generated.heights


def test_generator_reproducible(board):
    first = generate_dataset(per_category=2, seed=3821)
    second = generate_dataset(per_category=2, seed=3821)
    assert first == second
    assert len(first) == 6
    for item in first:
        assert len(item["move_history"]) == item["move_count"]
        assert replay(item["move_history"]).grid == item["grid"]
