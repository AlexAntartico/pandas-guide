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
├── charts/                                        ← Generated chart images
│   ├── chart01_revenue_trend.png
│   ├── chart02_revenue_by_region.png
│   ├── chart03_revenue_distribution.png
│   ├── chart04_stacked_bar.png
│   ├── chart05_scatter_units_revenue.png
│   ├── chart06_boxplot_region.png
│   ├── chart07_correlation_heatmap.png
│   └── chart08_dashboard.png
└── (total: ~3,600 lines across 18 files)
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
- Apply functions: apply, applymap, map
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

## Prerequisites
- Python 3.8+
- Basic Python knowledge (variables, functions, loops)
- No prior pandas experience required (but helpful)

## Libraries Used
- pandas (core)
- numpy (numerical operations)
- matplotlib (plotting)
- seaborn (statistical visualization)
- openpyxl (Excel reading/writing)
- xlsxwriter (Excel formatting)
- sqlalchemy (SQL operations)
- requests (API calls)
