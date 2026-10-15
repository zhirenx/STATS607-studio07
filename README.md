# Studio 07: scenario design and analysis

Work in teams of 2-4. Use `ASSIGNMENT.md` for the scientific questions.
The entire simulation engine is supplied. You complete four functions:

| File | Your work |
| --- | --- |
| `scenarios.py` | `make_scenarios()`: choose and construct the design |
| `analyze.py` | `summarize()`: means and Monte Carlo standard errors |
| `analyze.py` | `figure_a()`: reshape paired raw results and design figure A |
| `analyze.py` | `figure_b()`: prepare summaries and design figure B |

Replace the `raise NotImplementedError(...)` statements inside the task
markers. The plotting functions contain no axes, pivots, colors, labels,
or styling. Their docstrings specify the inputs and required outputs.

## Supplied components

- `src/dgps.py`: `NormalDGP` and `LaplaceDGP` implement `generate(rng)`.
- `src/methods.py`: `OLS` and `LAD` implement `fit(data, rng)`.
- `src/metrics.py`: the two losses and a `paired_ratio(lad, ols)` helper.
- `src/simulation.py`: `SimulationStudy`, random streams, saving, and resuming.
- `simulate.py`, analysis driver, Makefile, ADEMP description, and engine tests.

Read the components to connect this studio to last week's lecture. No
changes to the supplied engine are needed. The model has variance-one
errors, beta[j]=1/sqrt(p), and covariance[j,k]=rho**abs(j-k). Prediction loss
concerns the noiseless signal at new predictors from the same distribution.

## Scenario contract

`make_scenarios()` returns a dictionary mapping unique, stable,
filename-safe scenario IDs to parameter dictionaries. For example, this
is ONE scenario, not a complete design:

```python
{
    "A_normal_p040": {
        "experiment": "A", "n": 200, "p": 40,
        "rho": 0.0, "error_distribution": "normal"
    }
}
```

Each parameter dictionary has exactly these fields:

| Field | Contract |
| --- | --- |
| `experiment` | `"A"` or `"B"` |
| `n` | Integer sample size, 200 for this studio |
| `p` | Integer predictor count, `0 < p < n` |
| `rho` | AR(1) correlation, `0 <= rho < 1` |
| `error_distribution` | `"normal"` or `"laplace"` |

For A, hold rho=0 and compare both error distributions at the same chosen
aspect ratios. For B, hold p=100 and normal errors and vary rho. Choose a
manageable grid spanning small to large p/n and weak to strong correlation.
Predict the patterns before running. Refine the grid after a first plot if
useful, and explain your choices. Keep existing IDs when adding scenarios.

The interface to the completed engine is:

```python
study = SimulationStudy(scenarios, n_reps=100, seed=20261015)
runs = study.run()
```

The result has exactly `2 * len(scenarios) * n_reps` rows, including failed
fits if any: one per scenario, replicate, and method. Columns are:

```text
study_id, scenario_id, experiment, n, p, rho, error_distribution,
gamma, rep, method, coefficient_error, prediction_error,
status, message, elapsed_seconds
```

`gamma=p/n`, `rep` starts at zero, and methods are `"OLS"` and `"LAD"`.
Both methods use the same dataset in each replicate. Error columns contain
realized losses, not averages. Summaries retain total and successful fit
counts so any failures remain visible.

## Run the study

Use the course environment; if needed, install dependencies before class:

```bash
python3 -m pip install -r requirements.txt
make test
```

After completing `make_scenarios()`, check a small run, then launch the study:

```bash
make simulate REPS=2
make simulate REPS=100
make analyze
make figures
```

After all four functions are complete, `make all` runs the complete workflow.
`make analyze` and `make figures` use saved results without fitting models.
Use `make PYTHON=python` if that is your environment's Python command.
`make clean` removes generated results, including checkpoints.

## Start plotting by minute 10

Agree on the design together, then divide aggregation and the two figures.
Reference raw results and a summary are supplied so plotters can start while
the simulation runs or aggregation is unfinished:

```bash
python3 analyze.py --stage figures --input reference/runs.csv --figure A --out draft_a
python3 analyze.py --stage figures --input reference/runs.csv --summary reference/summary.csv --figure B --out draft_b
```

Figure A takes raw results so you can pair methods by scenario and replicate.
The supplied `paired_ratio` helper handles the paired uncertainty formula;
you still choose the reshaping and plotting. Figure B takes the summary
table specified in `summarize()`'s docstring. Approximate bars of +/-2 MCSE
show simulation uncertainty, not sampling intervals for beta.

## Outputs and reproducibility

`results/raw/runs.csv` is the current study's replicate table; `design.csv`
lists every chosen scenario, and `metadata.json` records the configuration,
master seed, stream rule, source hashes, and dependency versions. Each study
also has a folder named by its configuration/code fingerprint.

Within that folder, one CSV/NPZ pair checkpoints each completed scenario.
The NPZ saves estimates with shape `(n_reps, 2, p)`, method IDs, beta_true,
and covariance. Load it with `np.load(path, allow_pickle=False)` to recompute
losses without fitting again. Running the same command resumes completed
scenarios; an interrupted scenario is repeated as a batch. Changed code or
settings create a new study folder. Streams depend on the master seed,
scenario ID, replicate, and task, so reordering or adding scenarios does not
alter draws for an existing ID. Different scenario IDs use separate streams.

`results/summary.csv` contains your aggregated results. Figures are exported
to `results/figures/` as PNG and PDF, with analysis provenance. The supplied
reference files come from the completed example; identify their use if you
use them in your submission. Follow `ASSIGNMENT.md` for deliverables.
