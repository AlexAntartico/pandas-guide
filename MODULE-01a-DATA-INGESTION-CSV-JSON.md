# MODULE-01a: DATA INGESTION — CSV AND JSON

## The Data Loading Landscape

Real-world data comes in many formats. Pandas provides `read_*` functions for each:

| Function | Format | Best For |
|----------|--------|----------|
| `read_csv()` | CSV/TSV | Flat files, exports from systems |
| `read_json()` | JSON | APIs, NoSQL databases |
| `read_excel()` | Excel (.xlsx) | Business reports, spreadsheets |
| `read_sql()` | SQL databases | Relational databases |
| `read_parquet()` | Parquet | Big data, analytics pipelines |

---

## 1. CSV FILES — The Workhorse

### Basic Loading

```python
import pandas as pd

# Minimal — just the file path
df = pd.read_csv('data.csv')

# With TSV (tab-separated)
df = pd.read_csv('data.tsv', sep='\t')
```

> **JupyterLab:** Paths are relative to the directory where you launched `jupyter lab`, not the notebook file's location. Run `%pwd` in a cell to confirm, or use absolute paths. To get the notebook's own directory: `from pathlib import Path; here = Path().resolve()`.

### Critical Parameters (and WHY they matter)

```python
# --- HEADER & ROWS ---
df = pd.read_csv('data.csv',
    header=0,           # Row to use as column names (0 = first row)
                        # Why? Some files have metadata rows at top
    index_col=0,        # Column to use as row index
                        # Why? Faster lookups, meaningful labels
    skiprows=[1, 3],    # Skip specific row numbers (0-indexed)
    skipfooter=2,       # Skip rows at the end
    nrows=100,          # Only read first 100 rows
                        # Why? Preview large files without loading all
)

# --- DATA TYPES ---
df = pd.read_csv('data.csv',
    dtype={'age': 'int32', 'salary': 'float64'},
                        # Force specific types
                        # Why? Save memory, prevent type errors
    parse_dates=['created_date', 'updated_date'],
                        # Parse as datetime instead of string
                        # Why? Enable time-series operations
)

# --- MISSING VALUES ---
df = pd.read_csv('data.csv',
    na_values=['NA', 'N/A', '-', 'NULL', ''],
                        # Treat these strings as NaN
                        # Why? Different systems use different null markers
    keep_default_na=True,
)

# --- ENCODING ---
df = pd.read_csv('data.csv',
    encoding='utf-8',     # Standard encoding
    encoding='latin-1',   # For European characters
                        # Why? Wrong encoding = garbled text
)

# --- CHUNKING (Large Files) ---
# Why chunk? Files larger than RAM will crash your program
chunk_size = 100_000
chunks = []
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    filtered = chunk[chunk['status'] == 'active']
    chunks.append(filtered)
df = pd.concat(chunks, ignore_index=True)

> **JupyterLab:** Add a progress bar to chunk loops with `from tqdm.notebook import tqdm`, then wrap the iterator: `for chunk in tqdm(pd.read_csv('file.csv', chunksize=chunk_size), desc="Loading")`. Install with `!pip install tqdm`.

# --- USECOLS (Memory Optimization) ---
df = pd.read_csv('data.csv', usecols=['name', 'age', 'salary'])
                        # Why? Faster loading, less memory
```

### Common CSV Pitfalls

```python
# Problem: Comma in quoted fields
# Solution: Pandas handles this automatically with quotechar='"'

# Problem: Mixed line endings (Windows \r\n vs Unix \n)
# Solution: Use lineterminator='\n' or let pandas auto-detect

# Problem: Inconsistent number of fields
# Solution: on_bad_lines parameter
df = pd.read_csv('data.csv', on_bad_lines='warn')
                        # Options: 'error', 'warn', 'skip'
```

---

## 2. JSON FILES

JSON (JavaScript Object Notation) is hierarchical. Pandas needs help flattening it.

### Simple JSON (List of Dicts)

```python
# JSON array of objects → DataFrame directly
df = pd.read_json('data.json')

# From JSON string
import json
json_str = '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]'
df = pd.read_json(json_str)
```

### Nested JSON — The Real Challenge

```python
import json
from pandas import json_normalize

# Nested structure (common from APIs)
nested_data = {
    "users": [
        {
            "id": 1,
            "name": "Alice",
            "address": {"city": "NYC", "zip": "10001"},
            "orders": [{"id": 101, "amount": 50}, {"id": 102, "amount": 75}]
        },
        {
            "id": 2,
            "name": "Bob",
            "address": {"city": "LA", "zip": "90001"},
            "orders": [{"id": 103, "amount": 100}]
        }
    ]
}

# Method 1: json_normalize (flatten nested structures)
# Flatten one level
df = json_normalize(nested_data['users'])
print(df)
#    id   name address.city address.zip  ...
# 0   1  Alice          NYC       10001  ...
# 1   2    Bob           LA       90001  ...

# Flatten with record_path (extract nested lists)
df_orders = json_normalize(
    nested_data['users'],
    record_path='orders',          # The nested list to extract
    meta=['id', 'name',            # Columns to keep from parent
          ['address', 'city']]     # Nested parent columns
)
print(df_orders)
#    id  amount name address.city
# 0 101      50  Alice          NYC
# 1 102      75  Alice          NYC
# 2 103     100    Bob           LA
```

### JSON Orientation

```python
# Pandas can read JSON in different orientations
# 'records': [{"col": val}, ...]  (default, most common)
# 'split':   {"index": [...], "columns": [...], "data": [[...]]}
# 'index':   {row_idx: {col: val}}
# 'columns': {col: {row_idx: val}}
# 'values':  [[val, val], ...]

# Example: reading 'split' orientation
df = pd.read_json('data.json', orient='split')
```

---

## Quick Reference

| Task | Code |
|------|------|
| Load CSV | `pd.read_csv('file.csv')` |
| Load TSV | `pd.read_csv('file.tsv', sep='\t')` |
| Load JSON | `pd.read_json('file.json')` |
| Preview large file | `pd.read_csv('file.csv', nrows=100)` |
| Load specific columns | `pd.read_csv('file.csv', usecols=['a', 'b'])` |
| Parse dates | `pd.read_csv('file.csv', parse_dates=['date'])` |
| Handle missing values | `pd.read_csv('file.csv', na_values=['NA', '-'])` |
| Chunk large file | `pd.read_csv('file.csv', chunksize=10000)` |
| Flatten nested JSON | `json_normalize(data, record_path='items')` |

---

## Next Steps

- **Module 01b:** Excel, SQL, API, and Parquet loading
- **Module 02a:** Basic data exploration (EDA)
