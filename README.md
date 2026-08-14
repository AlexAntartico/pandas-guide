# 🐼 PANDAS MASTER GUIDE — ARCHITECTURE

## Structure Overview
This guide is divided into **9 modules** (some split into a/b for readability, ~300 lines each).

```
pandas-guide/
├── README.md                                     ← Overview + navigation
├── MODULE-00-GETTING-STARTED.md                  ← Setup, philosophy, core objects
├── MODULE-01a-DATA-INGESTION-CSV-JSON.md         ← Loading CSV and JSON
├── MODULE-01b-DATA-INGESTION-EXCEL-SQL-API.md    ← Loading Excel, SQL, APIs, Parquet
├── MODULE-02a-DATA-EXPLORATION-BASIC.md           ← First look, sampling, summary stats
├── MODULE-02b-DATA-EXPLORATION-ADVANCED.md        ← Correlation, distributions, EDA function
├── MODULE-03a-DATA-CLEANING-MISSING.md            ← Missing values: detection and imputation
├── MODULE-03b-DATA-CLEANING-PATTERNS.md           ← Duplicates, types, strings, outliers
├── MODULE-04a-DATA-MANIPULATION-INDEXING.md       ← Indexing, filtering, sorting, columns
├── MODULE-04b-DATA-MANIPULATION-GROUPBY-MERGE.md  ← GroupBy, merge, concat
├── MODULE-05a-DATA-TRANSFORMATION-PIVOT-RESHAPE.md ← Pivot tables, wide↔long reshaping
├── MODULE-05b-DATA-TRANSFORMATION-STRINGS-TIMESERIES.md ← Strings, DateTime, time series, categories
├── MODULE-06a-VISUALIZATION-BASIC.md              ← Line, bar, histogram charts
├── MODULE-06b-VISUALIZATION-ADVANCED.md           ← Scatter, box, heatmap, dashboards
├── MODULE-07a-DATA-EXPORT-CSV-EXCEL.md            ← CSV and styled Excel export
├── MODULE-07b-DATA-EXPORT-JSON-SQL-PARQUET.md     ← JSON, SQL, Parquet, production exporter
├── MODULE-08a-PRODUCTION-PERFORMANCE.md           ← Vectorization, memory, chunking
├── MODULE-08b-PRODUCTION-PATTERNS.md              ← Error handling, testing, best practices
├── datasets/                                      ← Practice data + exercise prompts
│   ├── generate_data.py                           ← Generator for the TechRetail scenario
│   ├── README.md                                  ← Scenario + 7-phase exercise prompts
│   ├── DQ-EDGE-CASES.md                           ← Catalog of intentional data issues
│   └── raw/                                       ← TechRetail Inc. multi-table data
│       ├── customers.csv / customers.json         ← Customer master (+ dirty records)
│       ├── products.csv                           ← Product catalog
│       ├── orders.csv / orders.parquet            ← Orders (CSV vs Parquet dtypes)
│       ├── order_items.csv                        ← Order line items
│       ├── payments.csv / payments.json           ← Payments (+ duplicates)
│       ├── shipments.csv                          ← Shipment tracking
│       ├── reviews.json                           ← Product reviews
│       ├── marketing_campaigns.csv                ← Campaign performance
│       ├── website_traffic.csv                    ← Daily traffic (with gaps)
│       ├── returns.csv                            ← Returns / refunds
│       └── data_dictionary.md                     ← Full schema reference
├── exercises/                                      ← Guided Jupyter notebooks (one per module)
│   ├── README.md                                  ← Notebook index + how to run
│   ├── generate_exercises.py                      ← Generator for the notebooks
│   ├── 00_getting_started.ipynb ... 08_production_performance.ipynb
├── charts/                                        ← Generated chart images
│   ├── chart01_revenue_trend.png ... chart08_dashboard.png
├── build_html.py                                  ← Builds pandas-guide.html
├── build_pdf.py                                   ← Builds Pandas-Master-Guide.pdf
└── (total: ~3,800 lines across 18 module files)
```

## Module Breakdown

### MODULE-00: GETTING STARTED
- Pandas philosophy and why it exists
- Core objects: Series, DataFrame, Index
- Installation and version management
- First DataFrame: creating from scratch

### MODULE-01: DATA INGESTION
- CSV: read_csv deep dive (all important parameters)
- JSON: read_json, nested JSON handling
- Excel: read_excel, multi-sheet, formatting
- SQL: read_sql, read_sql_query, connections
- APIs: fetching JSON from REST endpoints
- Parquet and other binary formats
- Error handling and chunking for large files

### MODULE-02: DATA EXPLORATION (Simple EDA)
- First look: head(), tail(), sample()
- Structure: info(), shape, columns, dtypes
- Summary statistics: describe()
- Value counts and distributions
- Correlation analysis
- Missing data overview
- Quick visual exploration

### MODULE-03: DATA CLEANING
- Missing values: detection, analysis, strategies
- Imputation methods (mean, median, forward fill, interpolation)
- Duplicate detection and removal
- Type conversion and validation
- String cleaning and normalization
- Outlier detection and handling
- Data validation patterns

### MODULE-04: DATA MANIPULATION
- Indexing and selection: loc, iloc, at, iat
- Boolean filtering and masking
- Sorting (single/multi column, ascending/descending)
- Column operations: add, drop, rename, reorder
- Apply functions: apply, map (applymap was deprecated in pandas 2.1)
- GroupBy operations: split-apply-combine
- Merge and join: inner, outer, left, right
- Concat and append

### MODULE-05: DATA TRANSFORMATION
- Pivot tables and crosstabs
- Melting and stacking (wide to long)
- String operations (str accessor)
- DateTime operations
- Time series resampling
- Window functions (rolling, expanding, exponential)
- Categorical data handling
- Feature engineering basics

### MODULE-06: VISUALIZATION
- Matplotlib fundamentals for pandas
- Built-in pandas plotting
- Professional line charts
- Bar charts (grouped, stacked)
- Histograms and density plots
- Scatter plots and bubble charts
- Box plots and violin plots
- Heatmaps and correlation matrices
- Time series visualization
- Subplots and multi-panel layouts
- Chart customization (colors, fonts, labels)
- Production-grade chart templates

### MODULE-07: DATA EXPORT
- CSV export: to_csv with formatting options
- Excel export: to_excel with styling (openpyxl, xlsxwriter)
- JSON export: to_json formats
- SQL export: to_sql
- Parquet export
- Multi-sheet Excel reports
- Formatted Excel reports with charts

### MODULE-08: PRODUCTION-GRADE
- Performance optimization
- Memory management
- Vectorization vs apply
- Chunking for large datasets
- Error handling patterns
- Logging and monitoring
- Testing data pipelines
- Reproducible workflows
- Best practices checklist

## Navigation
Each file is self-contained but references others. Start from MODULE-00 and progress sequentially, or jump to specific modules as needed.

## Practice Datasets
The guide ships with a realistic **TechRetail Inc.** e-commerce scenario in `datasets/raw/` — 10 interconnected tables (customers, products, orders, order items, payments, shipments, reviews, marketing campaigns, website traffic, returns) with *intentional* data-quality issues baked in.

- **`datasets/README.md`** — the scenario, a quick-start snippet, and 7 phases of exercise prompts (loading → DQ assessment → cleaning → EDA → multi-table → advanced → reporting).
- **`datasets/raw/data_dictionary.md`** — full schema reference for every table.
- **`datasets/DQ-EDGE-CASES.md`** — the catalog of every embedded data issue and what it exercises.

Every module links back to the relevant tables and exercise phase. Regenerate the data with:

```bash
python datasets/generate_data.py
```

> **Note:** the `datasets/` directory also contains an older, smaller scenario (`generate_datasets.py` → `clients.csv`, `promotions.tsv`, `transactions.json`). The TechRetail `raw/` scenario is the canonical one used by the modules.

Hands-on exercises that walk through real analyses live in a companion repository: https://github.com/AlexAntartico/pandas_practice

## Guided Exercises

The `exercises/` directory contains one Jupyter notebook per module (`00_getting_started.ipynb` … `08_production_performance.ipynb`). Each walks through the TechRetail datasets with step-by-step, commented code cells — launch `jupyter lab` from the repository root and open them. See `exercises/README.md` for the index and how to regenerate them.

## JupyterLab Usage
This guide is written for use in **JupyterLab**. Every module contains `> **JupyterLab:**` callout blocks that highlight notebook-specific behaviour: when to skip `print()`, how `%matplotlib inline` affects charts, path quirks, cell re-execution pitfalls, magic commands (`%%timeit`, `%pwd`, `%memit`), and more.

Install JupyterLab and launch it before working through the modules:
```bash
pip install jupyterlab
jupyter lab
```

The complete **JUPYTERLAB WORKFLOW** checklist is at the end of MODULE-08b.

## Prerequisites
- Python 3.8+
- Basic Python knowledge (variables, functions, loops)
- No prior pandas experience required (but helpful)
- JupyterLab (recommended) — all callouts in this guide target JupyterLab

## Libraries Used
- pandas (core)
- numpy (numerical operations)
- matplotlib (plotting)
- seaborn (statistical visualization)
- openpyxl (Excel reading/writing)
- xlsxwriter (Excel formatting)
- sqlalchemy (SQL operations)
- requests (API calls)
- jupyterlab (recommended IDE)
- tqdm (progress bars for chunk loops)
- ipympl (interactive `%matplotlib widget` charts)
