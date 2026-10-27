"""Generate reachable nonterminal Connect Four positions, grouped by move count.
The two requested categories mid/late intentionally overlap at move 27.

To actually generate 10 boards per category:
python3 -m Benchmarks.generate_boards --per-category 10 --seed 3821
"""
import argparse
import json
import random
from pathlib import Path

from connect_4 import Board

RANGES = {"early": (0, 13), "mid": (14, 27), "late": (27, 41)}


def replay(moves):
    board = Board()
    for col in moves:
        if col not in board.legal_moves() or board.check_win() or board.is_full():
            raise ValueError("Invalid move history")
        board.place_piece(col)
    return board


def generate_board(category, rng=None, target_moves=None, max_attempts=2000):
    """Produce a nonterminal reachable position; rng is an instance of random.Random.

    Within each attempt, we avoid immediately winning moves (ones htat are legal but not terminal), 
    so late positions are practical to generate. This implementation is technically not uniformly 
    random over reachable boards, and we should probably record this sampling policy in any experiment report.
    """
    if category not in RANGES:
        raise ValueError(f"Unknown category {category!r}")
    low, high = RANGES[category]
    if target_moves is not None and not low <= target_moves <= high:
        raise ValueError("Target outside category")
    rng = random.Random() if rng is None else rng
    for _ in range(max_attempts):
        target = target_moves if target_moves is not None else rng.randint(low, high)
        board = Board()
        moves = []
        for _ in range(target):
            safe = []
            for col in board.legal_moves():
                board.place_piece(col)
                if not board.check_win() and not board.is_full():
                    safe.append(col)
                board.undo()
            if not safe:
                break
            chosen = rng.choice(safe)
            board.place_piece(chosen)
            moves.append(chosen)
        if len(moves) == target and not board.check_win() and not board.is_full():
            return board, moves
    raise RuntimeError(f"Could not generate {category} target={target_moves} after {max_attempts} tries")


def generate_dataset(per_category=10, seed=3821):
    if per_category < 1:
        raise ValueError("per_category must be >= 1")
    rng = random.Random(seed)
    records = []
    seen = set()
    for category in RANGES:
        for index in range(per_category):
            for _ in range(500):
                board, moves = generate_board(category, rng)
                signature = tuple(tuple(row) for row in board.grid)
                if signature not in seen:
                    seen.add(signature)
                    break
            else:
                raise RuntimeError("Could not generate enough unique positions")
            records.append({"board_id": f"{category}_{index + 1:03d}",
                            "category": category, "move_count": len(moves),
                            "next_player": board.player_turn(),
                            "move_history": moves, "grid": board.grid,
                            "seed": seed})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-category", type=int, default=10)
    parser.add_argument("--seed", type=int, default=3821)
    parser.add_argument("--output", default="Benchmarks/positions.json")
    args = parser.parse_args()
    records = generate_dataset(args.per_category, args.seed)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(records)} positions to {path}")


if __name__ == "__main__":
    main()
