# Guided Exercises

Hands-on Jupyter notebooks that walk through the guide's modules using the
bundled **TechRetail Inc.** datasets (`datasets/raw/`). Each notebook poses
questions and guides you through the solution with step-by-step, commented code
cells — run every cell as you go.

## Running the exercises

```bash
# from the repository root
pip install jupyterlab
jupyter lab
```

Then open the `.ipynb` files under `exercises/`. The notebooks assume JupyterLab
is launched from the **repository root**, so the `datasets/raw/...` paths resolve
correctly (confirm with `%pwd`).

## Notebook index

| Notebook | Maps to | Covers | Exercise phase |
|----------|---------|--------|----------------|
| `00_getting_started.ipynb` | MODULE-00 | Series, DataFrame, `info()`, index | — |
| `01_data_ingestion.ipynb` | MODULE-01a/01b | CSV vs JSON vs Parquet, dtypes, `parse_dates`, TSV | Phase 1 |
| `02_data_exploration.ipynb` | MODULE-02a/02b | shape, `describe`, value counts, missing, correlation | Phases 1 & 4 |
| `03_data_cleaning.ipynb` | MODULE-03a/03b | missing, duplicates, types, strings, outliers | Phases 2 & 3 |
| `04_data_manipulation.ipynb` | MODULE-04a/04b | loc/iloc, filtering, sorting, groupby, merge | Phases 1, 2 & 5 |
| `05_data_transformation.ipynb` | MODULE-05a/05b | pivot, melt, strings, datetime, resample | Phases 3, 4 & 6 |
| `06_visualization.ipynb` | MODULE-06a/06b | line, bar, histogram, scatter, box, heatmap | Phases 4 & 7 |
| `07_data_export.ipynb` | MODULE-07a/07b | CSV, Excel, JSON, Parquet, SQL | Phase 7 |
| `08_production_performance.ipynb` | MODULE-08a/08b | vectorization, memory, chunking, error handling | Phases 3 & 6 |

The "Exercise phase" column refers to the prompts in `datasets/README.md`.

## Regenerating the notebooks

The notebooks are generated from a single source of truth:

```bash
python exercises/generate_exercises.py
```

## Reference

- `datasets/README.md` — the TechRetail scenario and all exercise prompts
- `datasets/raw/data_dictionary.md` — schema for every table
- `datasets/DQ-EDGE-CASES.md` — catalog of intentional data-quality issues
- The companion walkthrough repository: https://github.com/AlexAntartico/pandas_practice
