# MODULE-07b: DATA EXPORT — JSON, SQL, PARQUET, AND MORE

---

## 4. JSON Export

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

# --- BASIC EXPORT ---
df.to_json('output.json')
                        # Default: 'columns' orientation

# --- ORIENTATIONS ---
df.to_json('output.json', orient='records', indent=2)
# orient options:
# 'columns':   {column: {index: value}}  (default)
# 'records':   [{column: value}, ...]     (most common for APIs)
# 'index':     {index: {column: value}}
# 'split':     {index: [...], columns: [...], data: [[...]]}
# 'table':     {schema: {...}, data: [...]}  (Pandas schema)
# 'values':    [[value, value], ...]

# --- WITH PARAMETERS ---
df.to_json('output.json',
    orient='records',       # Array of objects
    indent=2,               # Pretty-print with 2-space indent
    date_format='iso',      # ISO 8601 date format
    date_unit='s',          # Date unit: 's', 'ms', 'us', 'ns'
    force_ascii=False,      # Allow non-ASCII characters
    double_precision=10,    # Float precision
)
```

---

## 5. SQL Export

```python
from sqlalchemy import create_engine

# Create database connection
engine = create_engine('sqlite:///output.db')
engine = create_engine('postgresql://user:pass@host:5432/dbname')
engine = create_engine('mysql+pymysql://user:pass@host:3306/dbname')

# --- BASIC EXPORT ---
df.to_sql('employees', engine, index=False)
                        # Creates table and inserts data

# --- WITH PARAMETERS ---
df.to_sql('employees', engine,
    if_exists='replace',    # 'fail', 'replace', 'append'
    index=False,
    index_label='emp_id',   # Name for index column
    chunksize=1000,         # Insert in chunks (for large data)
    dtype={                 # Specify column types
        'name': 'VARCHAR(100)',
        'age': 'INTEGER',
        'salary': 'DECIMAL(10,2)',
        'hire_date': 'DATE'
    },
    method='multi',         # 'multi': multi-row INSERT (faster)
)

# --- WHY CHUNKSIZE? ---
# Large inserts can timeout or run out of memory
# chunksize=1000: Insert 1000 rows at a time
# Trade-off: smaller = safer, larger = faster
```

---

## 6. Other Export Formats

```python
# --- PARQUET (columnar, compressed) ---
df.to_parquet('output.parquet', engine='pyarrow')
# Why parquet?
# - Columnar storage (fast for analytical queries)
# - Compression (smaller files)
# - Preserves data types
# - Industry standard for big data
```

> **JupyterLab:** Parquet is the best format for saving intermediate DataFrames between sessions — it's fast, compressed, and restores all dtypes (including `category`) exactly. Use `df.to_parquet('checkpoint.parquet')` / `df = pd.read_parquet('checkpoint.parquet')` as a notebook checkpoint pattern to avoid re-running expensive processing cells.

```python

# --- FEATHER (fast binary) ---
df.to_feather('output.feather')
# Why feather?
# - Very fast read/write
# - Preserves types
# - Language-agnostic (Python, R, Julia)

# --- PICKLE (Python-specific) ---
df.to_pickle('output.pkl')
# Why pickle?
# - Fastest for Python-only workflows
# - Preserves ALL pandas types
# - NOT portable to other languages
# - Security risk with untrusted data

# --- HTML ---
df.to_html('output.html', index=False, border=1)
# Why HTML?
# - Embed in web pages
# - Email reports
# - Documentation
```

> **JupyterLab:** Skip the file and render directly in the notebook: `from IPython.display import HTML; display(HTML(df.to_html(index=False, border=1)))`. Useful for embedding a styled table in a notebook report without creating a separate file.

```python

# --- LATEX (for papers) ---
df.to_latex('output.tex', index=False)
# Why LaTeX?
# - Academic papers
# - Professional documents
```

---

## 7. Production Export Pattern

```python
import logging
from pathlib import Path

def export_data(df, output_path: str, **kwargs):
    """
    Production-grade data exporter with validation and logging.
    
    Args:
        df: DataFrame to export
        output_path: Output file path
        **kwargs: Additional arguments for to_* functions
    """
    path = Path(output_path)
    
    # Validate DataFrame
    if df.empty:
        raise ValueError("Cannot export empty DataFrame")
    
    # Create output directory if needed
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Determine format from extension
    ext = path.suffix.lower()
    exporters = {
        '.csv': lambda: df.to_csv(path, index=False, **kwargs),
        '.tsv': lambda: df.to_csv(path, sep='\t', index=False, **kwargs),
        '.json': lambda: df.to_json(path, orient='records', indent=2, **kwargs),
        '.xlsx': lambda: df.to_excel(path, index=False, **kwargs),
        '.parquet': lambda: df.to_parquet(path, **kwargs),
        '.pkl': lambda: df.to_pickle(path, **kwargs),
    }
    
    if ext not in exporters:
        raise ValueError(f"Unsupported format: {ext}")
    
    try:
        exporters[ext]()
        file_size = path.stat().st_size
        logging.info(f"Exported {len(df)} rows to {output_path} ({file_size:,} bytes)")
    except Exception as e:
        logging.error(f"Failed to export to {output_path}: {e}")
        raise

# Usage
export_data(df, 'output/reports/employees.csv')
export_data(df, 'output/reports/employees.xlsx')
export_data(df, 'output/reports/employees.json')
```

---

## Quick Reference

| Task | Code |
|------|------|
| Export JSON | `df.to_json('file.json', orient='records')` |
| Export SQL | `df.to_sql('table', engine)` |
| Export Parquet | `df.to_parquet('file.parquet')` |
| Export Feather | `df.to_feather('file.feather')` |
| Export HTML | `df.to_html('file.html')` |
| Export Pickle | `df.to_pickle('file.pkl')` |

---

## Next Steps

- **Module 08a:** Performance optimization
- **Module 08b:** Production patterns and best practices

