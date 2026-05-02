# MODULE-01b: DATA INGESTION — EXCEL, SQL, APIs, AND MORE

---

## 3. EXCEL FILES

Excel files can contain multiple sheets, formatting, and formulas.

### Basic Loading

```python
import pandas as pd

# Single sheet
df = pd.read_excel('data.xlsx')              # First sheet by default
df = pd.read_excel('data.xlsx', sheet_name='Sheet2')
df = pd.read_excel('data.xlsx', sheet_name=0) # By index (0-based)

# Multiple sheets at once
sheets = pd.read_excel('data.xlsx', sheet_name=None)
                        # Returns dict: {sheet_name: DataFrame}
for name, df in sheets.items():
    print(f"Sheet: {name}, Shape: {df.shape}")
```

### Important Parameters

```python
df = pd.read_excel('data.xlsx',
    sheet_name='Data',
    header=0,               # Row for column names
    index_col=0,            # Column for row index
    usecols='A:D',          # Load specific columns (Excel notation)
    usecols=[0, 2, 3],      # Or by position
    skiprows=2,             # Skip header rows
    nrows=1000,             # Limit rows
    dtype={'ID': str},      # Force types
    parse_dates=['Date'],   # Parse date columns
    na_values=['NA', 'N/A', '-'],
    engine='openpyxl',      # For .xlsx files
    engine='xlrd',          # For .xls files (older format)
)
```

### Multi-Header Excel Files

```python
# Some Excel files have multi-row headers
df = pd.read_excel('data.xlsx', header=[0, 1])
                        # Creates MultiIndex columns
# Access: df[('Header1', 'SubHeader1')]
```

---

## 4. SQL DATABASES

```python
from sqlalchemy import create_engine

# Create engine (supports PostgreSQL, MySQL, SQLite, etc.)
engine = create_engine('sqlite:///mydatabase.db')
engine = create_engine('postgresql://user:pass@host:5432/dbname')
engine = create_engine('mysql+pymysql://user:pass@host:3306/dbname')

# Read SQL query
df = pd.read_sql("SELECT * FROM users WHERE active = 1", engine)

# Read entire table
df = pd.read_sql_table('users', engine)

# Read with parameters (prevents SQL injection)
df = pd.read_sql(
    "SELECT * FROM users WHERE department = %s",
    engine,
    params=['Engineering']
)

# Chunk large results
chunk_iter = pd.read_sql("SELECT * FROM large_table", engine, chunksize=10000)
for chunk in chunk_iter:
    process(chunk)
```

---

## 5. API DATA (JSON from REST APIs)

```python
import requests
from pandas import json_normalize

# Fetch data from API
response = requests.get('https://api.example.com/users')
response.raise_for_status()  # Raise error for bad responses
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data['results'])  # Adjust based on API structure

# Handle nested API responses
df = json_normalize(
    data['results'],
    record_path='items',
    meta=['page', 'total_count']
)
```

---

## 6. OTHER FORMATS

```python
# Parquet (columnar, compressed — best for big data)
df = pd.read_parquet('data.parquet')

# Feather (fast binary format)
df = pd.read_feather('data.feather')

# Pickle (Python-specific, fast but not portable)
df = pd.read_pickle('data.pkl')

# HTML tables (web scraping)
tables = pd.read_html('https://example.com/table-page.html')
                        # Returns list of DataFrames
df = tables[0]

# Clipboard (quick copy-paste)
df = pd.read_clipboard()  # Copy from Excel, paste directly
```

---

## Production-Grade Loading Pattern

```python
import pandas as pd
import logging
from pathlib import Path

def load_data_safely(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Production-grade data loader with error handling.
    
    Args:
        file_path: Path to data file
        **kwargs: Additional arguments passed to read_* functions
        
    Returns:
        DataFrame with loaded data
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Determine format from extension
    ext = path.suffix.lower()
    loaders = {
        '.csv': pd.read_csv,
        '.tsv': lambda p: pd.read_csv(p, sep='\t'),
        '.json': pd.read_json,
        '.xlsx': pd.read_excel,
        '.xls': pd.read_excel,
        '.parquet': pd.read_parquet,
    }
    
    if ext not in loaders:
        raise ValueError(f"Unsupported format: {ext}")
    
    try:
        df = loaders[ext](file_path, **kwargs)
        logging.info(f"Loaded {len(df)} rows, {len(df.columns)} columns from {file_path}")
        return df
    except Exception as e:
        logging.error(f"Failed to load {file_path}: {e}")
        raise

# Usage
df = load_data_safely('data/sales_2024.csv', parse_dates=['date'])
```

---

## Quick Reference

| Task | Code |
|------|------|
| Load Excel | `pd.read_excel('file.xlsx')` |
| Multiple sheets | `pd.read_excel('file.xlsx', sheet_name=None)` |
| Load SQL | `pd.read_sql('SELECT...', engine)` |
| Load from API | `pd.DataFrame(requests.get(url).json())` |
| Load Parquet | `pd.read_parquet('file.parquet')` |
| Load HTML table | `pd.read_html(url)` |
| Load from clipboard | `pd.read_clipboard()` |

---

## Next Steps

- **Module 02a:** Basic data exploration (EDA)
- **Module 07a:** Export to CSV and Excel
