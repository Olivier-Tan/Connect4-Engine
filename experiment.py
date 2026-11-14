
"""Temporary progression-check experiment using existing project modules.

Run from the Connect4-Engine project root:

python3 COMP3821_progress_experiment.py --per-category 10 --seed 3821 --depths 2 4 --repeats 3
"""

import argparse
import csv
from collections import defaultdict
from pathlib import Path

from Benchmarks.benchmarks import FIELDS, run
from Benchmarks.generate_boards import generate_dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-category", type=int, default=10)
    parser.add_argument("--seed", type=int, default=3821)
    parser.add_argument("--depths", type=int, nargs="+", default=[2, 4])
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument(
        "--output",
        default="results/progression_check_results.csv"
    )
    args = parser.parse_args()

    # Generate legal early, mid and late game positions.
    positions = generate_dataset(
        per_category=args.per_category,
        seed=args.seed
    )

    lookup = {p["board_id"]: p for p in positions}

    fixtures = {
        p["board_id"]: p["move_history"]
        for p in positions
    }

    # Benchmark minimax and alpha-beta on identical boards.
    rows = run(
        depths=args.depths,
        repeats=args.repeats,
        fixtures=fixtures
    )

    # Export all experimental results to CSV.
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["category", *FIELDS]

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow({
                "category": lookup[row["position"]]["category"],
                **row
            })

    print(
        f"Saved {len(rows)} experiment rows "
        f"from {len(positions)} boards to {output}"
    )

    # Group node counts by game stage and search depth.
    grouped = defaultdict(dict)

    for row in rows:
        key = (
            lookup[row["position"]]["category"],
            row["depth"]
        )

        grouped[key].setdefault(
            row["algorithm"], []
        ).append(row["nodes_evaluated"])

    # Print a summary of the results.
    print(
        "Category    Depth  Mean minimax nodes  "
        "Mean alpha-beta nodes  Reduction"
    )

    for category in ("early", "mid", "late"):
        for depth in args.depths:
            values = grouped[(category, depth)]

            if not all(
                k in values for k in ("minimax", "alpha_beta")
            ):
                continue

            mm = sum(values["minimax"]) / len(values["minimax"])
            ab = sum(values["alpha_beta"]) / len(values["alpha_beta"])

            reduction = 100 * (1 - ab / mm)

            print(
                f"{category:<11} {depth:<6} "
                f"{mm:>18.1f} {ab:>21.1f} "
                f"{reduction:>9.1f}%"
            )


if __name__ == "__main__":
    main()
