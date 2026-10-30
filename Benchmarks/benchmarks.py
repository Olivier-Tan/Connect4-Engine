"""Run repeatable minimax/alpha-beta benchmarks from the repository root.

Usage: python3 -m Benchmarks.run_benchmarks --depths 2 4 --repeats 3
"""
import argparse
import csv
import statistics
import time
from pathlib import Path

from connect_4 import Board
from Algorithms.minimax import minimax
from Algorithms.alpha_beta import alpha_beta

# Known legal, nonterminal fixtures, independent of the random generator.
FIXTURES = {
    "empty": [],
    "early": [3, 2, 3, 4],
    "mid": [3, 2, 3, 4, 4, 5, 1, 2, 5, 6, 0, 1, 2, 5],
}
ALGORITHMS = {"minimax": minimax, "alpha_beta": alpha_beta}
FIELDS = ["position", "move_count", "algorithm", "depth", "score",
          "nodes_evaluated", "runtime_ms_median", "runtime_ms_min", "repeats"]


def make_board(moves):
    board = Board()
    for col in moves:
        if board.check_win() or board.is_full() or col not in board.legal_moves():
            raise ValueError("Fixture has illegal or post-terminal move")
        board.place_piece(col)
    if board.check_win() or board.is_full():
        raise ValueError("Fixture must be nonterminal")
    return board


def measure(algorithm, board, depth, repeats=3):
    if repeats < 1 or depth < 0:
        raise ValueError("repeats >= 1 and depth >= 0 required")
    initial = ([row[:] for row in board.grid], board.heights[:], board.history[:])
    times, scores, counts = [], [], []
    for _ in range(repeats):
        # Rebuild from history to rule out mutation leaking between trials.
        trial = make_board([col for _, col in board.history])
        start = time.perf_counter()
        _, score, stats = algorithm(trial, depth, True, trial.player_turn())
        times.append((time.perf_counter() - start) * 1000)
        scores.append(score)
        counts.append(stats["nodes_evaluated"])
        if trial.grid != initial[0] or trial.heights != initial[1] or trial.history != initial[2]:
            raise AssertionError("Search mutated its input board")
    if len(set(scores)) != 1 or len(set(counts)) != 1:
        raise AssertionError("Non-deterministic score or node count")
    return {"score": scores[0], "nodes_evaluated": counts[0],
            "runtime_ms_median": statistics.median(times),
            "runtime_ms_min": min(times), "repeats": repeats}


def run(depths=(2, 4), repeats=3, fixtures=None):
    fixtures = FIXTURES if fixtures is None else fixtures
    rows = []
    for name, moves in fixtures.items():
        board = make_board(moves)
        for depth in depths:
            scores = {}
            for algo_name, algorithm in ALGORITHMS.items():
                measurement = measure(algorithm, board, depth, repeats)
                scores[algo_name] = measurement["score"]
                rows.append({"position": name, "move_count": len(moves),
                             "algorithm": algo_name, "depth": depth, **measurement})
            if len(set(scores.values())) != 1:
                raise AssertionError(f"Search scores disagree: {name}, depth {depth}: {scores}")
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depths", type=int, nargs="+", default=[2, 4])
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", default="results/benchmark_results.csv")
    args = parser.parse_args()
    rows = run(args.depths, args.repeats)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} results to {path}")


if __name__ == "__main__":
    main()
