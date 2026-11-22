"""Generate two editable COMP3821 poster figures from your own benchmark CSV.

Place this file next to experiment.py in the Connect4-Engine project, and run:
    python make_my_poster_graphs.py

Input:  results/four_way_final.csv
Output: poster_figures/nodes_depth4.pdf/.png, runtime_depth4.pdf/.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DEPTH = 4
LOG_SCALE = True  # Helps show both large early-game and small late-game values.

STAGES = ["early", "mid", "late"]
ALGORITHMS = ["minimax", "alpha_beta", "alpha_beta_center", "alpha_beta_heuristic"]
DISPLAY_NAMES = {
    "minimax": "Minimax",
    "alpha_beta": "Alpha-beta",
    "alpha_beta_center": "Centre-first",
    "alpha_beta_heuristic": "Heuristic",
}

csv_file = Path("results/four_way_final.csv")
if not csv_file.exists():
    raise SystemExit(f"Could not find {csv_file}. Run this from the project root.")

df = pd.read_csv(csv_file)
if not df.groupby(["position", "depth"])["score"].nunique().eq(1).all():
    raise SystemExit("Algorithms disagree on scores for at least one position/depth; check correctness first.")

depth_results = df[df["depth"] == DEPTH]
if depth_results.empty:
    raise SystemExit(f"No experiment rows at depth {DEPTH}.")

output_folder = Path("poster_figures")
output_folder.mkdir(exist_ok=True)


def plot_mean(metric, title, ylabel, filename):
    summary = (
        depth_results.groupby(["category", "algorithm"])[metric]
        .mean()
        .unstack()
        .reindex(index=STAGES, columns=ALGORITHMS)
    )
    if summary.isna().any().any():
        raise SystemExit("Missing a category/algorithm result in the CSV.")
    summary.columns = [DISPLAY_NAMES[name] for name in summary.columns]
    summary.index = [name.title() for name in summary.index]

    ax = summary.plot(kind="bar", figsize=(9.5, 4.5), width=0.78, logy=LOG_SCALE, rot=0)
    ax.set_title(title, fontsize=14, weight="bold", pad=12)
    ax.set_xlabel("Game stage")
    ax.set_ylabel(ylabel + (" (log scale)" if LOG_SCALE else ""))
    ax.grid(axis="y", which="both", alpha=0.2)
    ax.set_axisbelow(True)
    ax.legend(title="Algorithm", ncol=2, fontsize=9, title_fontsize=9, loc="upper right")
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(output_folder / f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(output_folder / f"{filename}.png", dpi=240, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved poster_figures/{filename}.pdf and .png")
    print(summary.round(2).to_string(), "\n")


# Mean node counts over the 10 board positions in each game stage.
plot_mean(
    metric="nodes_evaluated",
    title=f"Search nodes visited at depth {DEPTH}",
    ylabel="Mean nodes visited",
    filename=f"nodes_depth{DEPTH}",
)

# Each CSV runtime is the median of three repeated trials; we average those
# per-position medians across the 10 board positions in each stage.
plot_mean(
    metric="runtime_ms_median",
    title=f"Execution time at depth {DEPTH}",
    ylabel="Mean per-position median runtime (ms)",
    filename=f"runtime_depth{DEPTH}",
)

print("Check graph axes and captions before adding these figures to Overleaf.")
