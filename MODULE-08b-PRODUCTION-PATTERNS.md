# MODULE-08b: PRODUCTION-GRADE PANDAS — PATTERNS AND BEST PRACTICES

---

## 3. Error Handling Patterns

```python
import logging
from pathlib import Path

def safe_load_and_process(file_path):
    """Production-grade data loading with error handling."""
    logging.basicConfig(level=logging.INFO)
    
    # 1. Validate file exists
    path = Path(file_path)
    if not path.exists():
        logging.error(f"File not found: {file_path}")
        return None
    
    # 2. Load with error handling
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loaded {len(df)} rows")
    except pd.errors.ParserError as e:
        logging.error(f"Parse error: {e}")
        return None
    except Exception as e:
        logging.error(f"Load error: {e}")
        return None
    
    # 3. Validate data
    if df.empty:
        logging.warning("Empty DataFrame loaded")
        return None
    
    required_cols = ['id', 'value']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        logging.error(f"Missing columns: {missing_cols}")
        return None
    
    # 4. Process with validation
    try:
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna(subset=['value'])
        logging.info(f"Processed {len(df)} valid rows")
    except Exception as e:
        logging.error(f"Processing error: {e}")
        return None
    
    return df
```

---

## 4. Testing Data Pipelines

```python
# --- ASSERTIONS FOR DATA VALIDATION ---
def validate_dataframe(df):
    """Validate DataFrame meets expectations."""
    assert len(df) > 0, "DataFrame is empty"
    assert 'id' in df.columns, "Missing 'id' column"
    assert df['id'].is_unique, "Duplicate IDs found"
    assert df['value'].notna().all(), "Missing values in 'value'"
    assert (df['value'] >= 0).all(), "Negative values found"
    assert df['date'].is_monotonic_increasing, "Dates not sorted"
    print("✓ All validations passed")

# --- PROPERTY-BASED TESTING ---
def test_pipeline():
    """Test that pipeline preserves key properties."""
    # Load raw data
    raw = pd.read_csv('raw_data.csv')
    
    # Run pipeline
    cleaned = clean_data(raw)
    
    # Verify properties
    assert len(cleaned) <= len(raw), "Pipeline added rows"
    assert set(cleaned.columns) == set(raw.columns), "Columns changed"
    assert cleaned['id'].nunique() == len(cleaned), "Duplicates introduced"
    print("✓ Pipeline tests passed")
```

---

## 5. Reproducible Workflows

```python
# --- SET RANDOM SEED ---
import numpy as np
np.random.seed(42)
pd.options.mode.copy_on_write = True  # pandas 2.0+

# --- VERSION PINNING ---
# requirements.txt:
# pandas==2.2.0
# numpy==1.26.0
# matplotlib==3.8.0
# seaborn==0.13.0

# --- REPRODUCIBLE DATE HANDLING ---
# Always specify timezone
df['date'] = pd.to_datetime(df['date'], utc=True)
# Always specify date format
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# --- LOGGING ---
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

def run_pipeline():
    logging.info("Starting pipeline")
    df = load_data('input.csv')
    logging.info(f"Loaded {len(df)} rows")
    
    df = clean_data(df)
    logging.info(f"Cleaned: {len(df)} rows")
    
    df = transform_data(df)
    logging.info(f"Transformed: {len(df)} rows")
    
    export_data(df, 'output.csv')
    logging.info("Pipeline complete")
```

---

## 6. Best Practices Checklist

```python
"""
PANDAS PRODUCTION CHECKLIST
===========================

DATA LOADING:
☐ Use usecols to load only needed columns
☐ Specify dtypes to save memory
☐ Use parse_dates for date columns
☐ Handle encoding explicitly
☐ Use chunksize for large files

DATA CLEANING:
☐ Check for missing values before processing
☐ Validate data types after loading
☐ Use errors='coerce' for numeric conversion
☐ Handle duplicates explicitly
☐ Validate business rules (no negative ages, etc.)

DATA MANIPULATION:
☐ Prefer vectorized operations over apply
☐ Use .loc for label-based selection
☐ Use .iloc for position-based selection
☐ Chain operations when possible
☐ Use query() for complex filters

MEMORY MANAGEMENT:
☐ Downcast numerical types
☐ Use categorical for low-cardinality strings
☐ Drop unused columns early
☐ Use chunking for large datasets
☐ Monitor memory usage with memory_usage()

PERFORMANCE:
☐ Profile with %timeit or time
☐ Use vectorization first
☐ Use numba for complex functions
☐ Avoid iterrows() and itertuples()
☐ Use .values for numpy operations

VISUALIZATION:
☐ Set professional style (seaborn)
☐ Use appropriate chart types
☐ Add labels, titles, legends
☐ Format numbers (currency, percentages)
☐ Save in multiple formats (PNG, PDF)

EXPORT:
☐ Always use index=False for CSV/Excel
☐ Specify encoding (utf-8)
☐ Use appropriate date formats
☐ Validate output before sharing
☐ Log export details (rows, size)

GENERAL:
☐ Use copy() when modifying DataFrames
☐ Handle errors with try/except
☐ Log all operations
☐ Version pin dependencies
☐ Write tests for critical functions
"""
```

---

## 7. Common Pitfalls and Solutions

```python
# --- PITFALL 1: SettingWithCopyWarning ---
# WRONG: Creates warning, may not modify original
df[df['age'] > 30]['salary'] = 100000

# RIGHT: Use .loc
df.loc[df['age'] > 30, 'salary'] = 100000

# --- PITFALL 2: Chained Indexing ---
# WRONG: Slow, may fail
df['A'][0] = 10

# RIGHT: Use .loc or .iloc
df.loc[0, 'A'] = 10
df.iloc[0, 0] = 10

# --- PITFALL 3: Comparing Floats ---
# WRONG: Floating point precision issues
df[df['value'] == 0.1]

# RIGHT: Use np.isclose
df[np.isclose(df['value'], 0.1)]

# --- PITFALL 4: Modifying While Iterating ---
# WRONG: Unpredictable behavior
for idx, row in df.iterrows():
    df.loc[idx, 'new_col'] = row['a'] + row['b']

# RIGHT: Vectorized
df['new_col'] = df['a'] + df['b']

# --- PITFALL 5: Large Memory Usage ---
# WRONG: Loading everything into memory
df = pd.read_csv('large_file.csv')  # May crash

# RIGHT: Chunk or use PyArrow
for chunk in pd.read_csv('large_file.csv', chunksize=100_000):
    process(chunk)
```

---

## 8. Copy-on-Write (pandas 2.0+)

```python
# Enable copy-on-write (default in pandas 3.0+)
pd.options.mode.copy_on_write = True

# Why copy-on-write?
# - Prevents SettingWithCopyWarning
# - Makes DataFrame behavior more predictable
# - Slight performance cost but safer

# Before CoW (pandas < 2.0):
# df['new'] = value  # May modify original or copy

# After CoW (pandas >= 2.0 with CoW enabled):
# df['new'] = value  # Always creates new DataFrame
# Original is never modified unexpectedly
```

---

## 🎓 CONGRATULATIONS!

You've completed the comprehensive pandas guide. You now have knowledge from beginner to production-grade pandas usage.

### What You've Learned

| Module | Topics |
|--------|--------|
| 00 | Core objects (Series, DataFrame, Index) |
| 01 | Data ingestion (CSV, JSON, Excel, SQL, APIs) |
| 02 | Exploratory data analysis (EDA) |
| 03 | Data cleaning (missing values, duplicates, types) |
| 04 | Data manipulation (filtering, grouping, merging) |
| 05 | Data transformation (pivot, reshape, strings, time series) |
| 06 | Professional visualization (charts, dashboards) |
| 07 | Data export (CSV, Excel, JSON, SQL, Parquet) |
| 08 | Production patterns (performance, memory, best practices) |

### Resources

| Resource | Link |
|----------|------|
| Official Documentation | https://pandas.pydata.org/docs/ |
| 10 Minutes to Pandas | https://pandas.pydata.org/docs/user_guide/10min.html |
| Python for Data Analysis (Wes McKinney) | https://wesmckinney.com/book/ |
| Python Data Science Handbook (Jake VanderPlas) | https://jakevdp.github.io/PythonDataScienceHandbook/ |
| Pandas Cookbook | https://github.com/jvns/pandas-cookbook |
| Effective Pandas | https://github.com/mattharrison/effective_pandas |
| 100 Pandas Puzzles | https://github.com/ajcr/100-pandas-puzzles |

