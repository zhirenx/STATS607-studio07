"""Aggregate raw results and create two scientific comparison figures."""

import argparse
import hashlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.metrics import paired_ratio
from src.simulation import save_csv, save_json


def summarize(runs):
    """Return one summary row per scenario and method.

    Keep identifying columns study_id, scenario_id, experiment, n, p,
    gamma, rho, error_distribution, method. Add n_total (all fits), n_ok
    (nonmissing coefficient losses), coefficient_mse, prediction_mse,
    coefficient_mcse, prediction_mcse. Means use successful fits; each
    MCSE is the sample SD divided by sqrt(the number of nonmissing losses).
    Report failures: n_total - n_ok. Do not average over scenarios.
    """
    # BEGIN TASK SUMMARY
    group_cols = [
        "study_id", "scenario_id", "experiment",
        "n", "p", "gamma", "rho",
        "error_distribution", "method",
    ]

    summary = (
        runs.groupby(group_cols, dropna=False, sort=True)
        .agg(
            n_total=("coefficient_error", "size"),
            n_ok=("coefficient_error", "count"),
            coefficient_mse=("coefficient_error", "mean"),
            prediction_mse=("prediction_error", "mean"),
            coefficient_sd=("coefficient_error", "std"),
            prediction_sd=("prediction_error", "std"),
            n_prediction=("prediction_error", "count"),
        )
        .reset_index()
    )

    # Monte Carlo SE
    summary["coefficient_mcse"] = (
        summary["coefficient_sd"] / np.sqrt(summary["n_ok"])
    )
    summary["prediction_mcse"] = (
        summary["prediction_sd"] / np.sqrt(summary["n_prediction"])
    )

    summary = summary.drop(
        columns=["coefficient_sd", "prediction_sd", "n_prediction"]
    )

    return summary
    # END TASK SUMMARY


def figure_a(runs):
    """Return a matplotlib Figure for the MLE question, using RAW results.

    Use experiment A. Plot mean LAD coefficient loss / mean OLS coefficient
    loss against gamma, with normal/Laplace panels and a reference at one.
    Pair methods by (scenario_id, rep), keeping complete pairs. The supplied
    paired_ratio(lad, ols) returns the ratio and its paired MCSE; show about
    +/-2 MCSE. At least two complete pairs per scenario are needed.

    Choose all filtering, reshaping, axes, labels, scales, colors, and other
    formatting. Do not average replicate ratios or save files here.
    """
    # BEGIN TASK FIGURE_A
    experiment = runs.loc[
        (runs["experiment"] == "A") & runs["method"].isin(["OLS", "LAD"])
    ].copy()
    # Failed/nonfinite losses cannot contribute to a complete pair.
    valid = (experiment["status"] == "ok") & np.isfinite(experiment["coefficient_error"])
    experiment.loc[~valid, "coefficient_error"] = np.nan
    rows = []
    for (scenario_id, distribution, gamma), group in experiment.groupby(
        ["scenario_id", "error_distribution", "gamma"]
    ):
        pairs = group.pivot(index="rep", columns="method", values="coefficient_error")
        pairs = pairs.reindex(columns=["LAD", "OLS"]).dropna()
        if len(pairs) < 2:
            raise ValueError(f"Scenario {scenario_id!r} needs at least two complete pairs.")
        ratio, mcse = paired_ratio(pairs["LAD"].to_numpy(), pairs["OLS"].to_numpy())
        rows.append({"error_distribution": distribution, "gamma": gamma,
                     "ratio": ratio, "mcse": mcse})
    ratios = pd.DataFrame(rows)

    fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
    for ax, distribution, title in zip(
        axes, ["normal", "laplace"],
        ["Normal errors", "Laplace errors"]
    ):
        panel = ratios.loc[ratios["error_distribution"] == distribution].sort_values("gamma")
        ax.axhline(1, label="Equal MSE")
        ax.errorbar(panel["gamma"], panel["ratio"], yerr=2 * panel["mcse"],
                    label="Ratio ± 2 MCSE")
        ax.set(title=title, xlabel=r"Aspect ratio $\gamma = p/n$")
    axes[0].set_ylabel("Coefficient MSE ratio (LAD / OLS)")
    axes[0].legend()
    return fig
    # END TASK FIGURE_A


def figure_b(summary):
    """Return a matplotlib Figure for the estimation/prediction question.

    Use the summary DataFrame from summarize(), restricted to experiment B.
    Plot coefficient MSE and prediction MSE against rho in adjacent panels,
    with both methods and uncertainty based on the MCSEs (about +/-2 MCSE).
    Choose all data preparation, axes, labels, legends, scales, and styling.
    Do not save files here.
    """
    # BEGIN TASK FIGURE_B
    raise NotImplementedError('Prepare summary data and design figure B.')
    # END TASK FIGURE_B


def main():
    """Supplied driver: run stages separately without refitting methods."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["analyze", "figures", "all"], default="all")
    parser.add_argument("--input", type=Path, default=Path("results/raw/runs.csv"))
    parser.add_argument("--summary", type=Path, default=Path("results/summary.csv"))
    parser.add_argument("--figure", choices=["A", "B", "both"], default="both")
    parser.add_argument("--out", type=Path, default=Path("results/figures"))
    args = parser.parse_args()
    runs = pd.read_csv(args.input)
    failed = (runs.status == "failed").sum()
    print(f"Raw results: {len(runs):,} fits; {failed} failed fits retained.")
    provenance = {
        "raw_input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "analysis_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {"numpy": np.__version__, "pandas": pd.__version__,
                        "matplotlib": matplotlib.__version__},
        "uncertainty": "error bars are +/-2 Monte Carlo standard errors; paired ratio in A",
    }
    if args.stage in ["analyze", "all"]:
        summary = summarize(runs)
        save_csv(summary, args.summary)
        save_json(provenance, args.summary.with_suffix(".metadata.json"))
    if args.stage in ["figures", "all"]:
        args.out.mkdir(parents=True, exist_ok=True)
        if args.figure in ["A", "both"]:
            fig = figure_a(runs)
            fig.savefig(args.out / "figure_A.png", dpi=300)
            fig.savefig(args.out / "figure_A.pdf")
            plt.close(fig)
        if args.figure in ["B", "both"]:
            summary = pd.read_csv(args.summary)
            fig = figure_b(summary)
            fig.savefig(args.out / "figure_B.png", dpi=300)
            fig.savefig(args.out / "figure_B.pdf")
            plt.close(fig)
            provenance["summary_input_sha256"] = hashlib.sha256(args.summary.read_bytes()).hexdigest()
        save_json(provenance, args.out / "metadata.json")


if __name__ == "__main__":
    main()
