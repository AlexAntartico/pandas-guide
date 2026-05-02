# MODULE-08a: PRODUCTION-GRADE PANDAS — PERFORMANCE

## Production vs Notebook

Notebook code works for exploration. Production code must be:
- **Fast** — handles large datasets efficiently
- **Robust** — handles errors gracefully
- **Maintainable** — readable, documented, testable
- **Reproducible** — same input → same output

---

## 1. Performance Optimization

### Vectorization: The #1 Rule

```python
import pandas as pd
import numpy as np
import time

# Create large dataset
np.random.seed(42)
df = pd.DataFrame({
    'a': np.random.randn(1_000_000),
    'b': np.random.randn(1_000_000),
    'c': np.random.choice(['A', 'B', 'C'], 1_000_000)
})

# --- SLOW: Python loop ---
start = time.time()
result = []
for i in range(len(df)):
    result.append(df['a'].iloc[i] + df['b'].iloc[i])
df['sum_loop'] = result
print(f"Loop: {time.time() - start:.4f}s")

# --- SLOW: apply ---
start = time.time()
df['sum_apply'] = df.apply(lambda row: row['a'] + row['b'], axis=1)
print(f"apply: {time.time() - start:.4f}s")

# --- FAST: Vectorized ---
start = time.time()
df['sum_vec'] = df['a'] + df['b']
print(f"Vectorized: {time.time() - start:.4f}s")

# Vectorized operations are 10-100x faster because:
# 1. No Python loop overhead
# 2. numpy operations execute in C
# 3. Memory access is sequential (cache-friendly)
```

### When Vectorization Isn't Enough

```python
# --- NUMBA FOR COMPLEX FUNCTIONS ---
from numba import jit
import numpy as np

@jit(nopython=True)
def complex_calc(a, b):
    """JIT-compiled function for complex math."""
    return np.sin(a) * np.cos(b) + np.exp(-a**2)

start = time.time()
df['numba_result'] = complex_calc(df['a'].values, df['b'].values)
print(f"Numba: {time.time() - start:.4f}s")
```

### Chunking for Large Files

```python
# --- PROCESS IN CHUNKS ---
def process_large_file(file_path, chunk_size=100_000):
    """Process file in chunks to manage memory."""
    results = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process each chunk
        filtered = chunk[chunk['status'] == 'active']
        aggregated = filtered.groupby('category').agg({
            'revenue': ['sum', 'mean', 'count']
        })
        results.append(aggregated)
    
    # Combine results
    final = pd.concat(results).groupby(level=0).agg({
        ('revenue', 'sum'): 'sum',
        ('revenue', 'mean'): 'mean',
        ('revenue', 'count'): 'sum'
    })
    return final

# Why chunking?
# - Files larger than RAM will crash
# - Process one chunk at a time
# - Aggregate incrementally
```

---

## 2. Memory Optimization

### Check Current Memory Usage

```python
# --- MEMORY PROFILE ---
print(df.memory_usage(deep=True))
# deep=True: Include actual object sizes (strings, etc.)

# --- TOTAL MEMORY ---
total_mb = df.memory_usage(deep=True).sum() / 1024**2
print(f"Total: {total_mb:.1f} MB")
```

### Downcast Numerical Types

```python
# --- DOWNCAST INTEGERS ---
# int64 → int8/int16/int32 (if values fit)
df['small_int'] = pd.to_numeric(df['small_int'], downcast='integer')
# int64 (8 bytes) → int8 (1 byte): 8x memory savings

# --- DOWNCAST FLOATS ---
# float64 → float32
df['float_col'] = pd.to_numeric(df['float_col'], downcast='float')
# float64 (8 bytes) → float32 (4 bytes): 2x memory savings

# --- SPECIFIC DOWNSCASTING ---
def downcast_dataframe(df):
    """Aggressively downcast all numerical columns."""
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    return df

df_optimized = downcast_dataframe(df)
```

### Use Categorical for Low-Cardinality Strings

```python
# --- BEFORE: object dtype ---
print(df['category_col'].dtype)  # object
print(df['category_col'].memory_usage(deep=True))  # ~large

# --- AFTER: category dtype ---
df['category_col'] = df['category_col'].astype('category')
print(df['category_col'].dtype)  # category
print(df['category_col'].memory_usage(deep=True))  # ~small

# Memory savings = (unique_values / total_values) * original_size
# For 1M rows with 5 unique values: ~200,000x savings
```

### Optimize Data Loading

```python
# --- LOAD ONLY WHAT YOU NEED ---
# Use columns
df = pd.read_csv('data.csv', usecols=['col1', 'col2', 'col3'])

# Use dtypes
df = pd.read_csv('data.csv', dtype={
    'id': 'int32',
    'category': 'category',
    'value': 'float32'
})

# Use parse_dates
df = pd.read_csv('data.csv', parse_dates=['date_col'])

# Why optimize at load time?
# - Less memory from the start
# - Faster loading (less data to process)
# - No need to convert later
```

---

## Quick Reference

| Optimization | Code | Impact |
|-------------|------|--------|
| Vectorization | `df['a'] + df['b']` | 10-100x faster |
| Downcast int | `pd.to_numeric(col, downcast='integer')` | 2-8x less memory |
| Downcast float | `pd.to_numeric(col, downcast='float')` | 2x less memory |
| Categorical | `col.astype('category')` | 10-100x less memory |
| Chunking | `read_csv(chunksize=100000)` | Enables large file processing |
| usecols | `read_csv(usecols=['a','b'])` | Faster load, less memory |

---

## Next Steps

- **Module 08b:** Error handling, testing, best practices
- **Module 07a:** Export to CSV and Excel

