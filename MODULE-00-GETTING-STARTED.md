# MODULE-00: GETTING STARTED WITH PANDAS

## Why Pandas Exists

Pandas was created by **Wes McKinney** in 2008 while working at quantitative trading firms. He needed a tool that combined:
- The data manipulation power of Excel/SQL
- The flexibility of Python
- The performance of compiled languages

**Why pandas over pure Python lists/dicts?**
- Vectorized operations (no slow Python loops)
- Built-in handling of missing data (NaN)
- Labeled axes (column names, row indices)
- Time-series functionality
- Seamless integration with numpy, matplotlib, scipy

---

## Installation

```bash
# Minimal installation
pip install pandas

# Recommended full installation
pip install pandas numpy matplotlib seaborn openpyxl xlsxwriter sqlalchemy requests

# Verify installation
python -c "import pandas; print(pandas.__version__)"
```

**Version note:** This guide targets pandas 2.x. Some behaviors differ in 1.x.

---

## Core Philosophy

Pandas is built on three principles:

1. **Labeled data** — Every row and column has a name (index)
2. **Missing data is first-class** — NaN values are handled gracefully
3. **Vectorization** — Operations apply to entire columns at once (fast)

```python
import pandas as pd
import numpy as np

# Standard import convention — always use these aliases
# pd = pandas (the library)
# np = numpy (numerical computing foundation)
```

---

## The Three Core Objects

### 1. Series — 1D Labeled Array

A Series is like a column in a spreadsheet. It has:
- **Values** (the data)
- **Index** (labels for each value)

```python
# Creating a Series
s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print(s)
# a    10
# b    20
# c    30
# d    40
# dtype: int64

# Access by label
print(s['a'])      # 10
print(s[['a', 'c']])  # Multiple values

# Access by position
print(s.iloc[0])   # 10 (first position)
print(s.loc['a'])  # 10 (by label)
```

**Why index matters:** The index lets you align data automatically during operations.

```python
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([4, 5, 6], index=['b', 'c', 'd'])
print(s1 + s2)  # Automatic alignment by index
# a    NaN  (only in s1)
# b    6.0  (1 + 5)
# c    8.0  (2 + 6)
# d    NaN  (only in s2)
```

### 2. DataFrame — 2D Labeled Table

A DataFrame is like a spreadsheet or SQL table. It's a collection of Series that share an index.

```python
# Creating a DataFrame from dict
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

print(df)
#      name  age  salary
# 0   Alice   25   50000
# 1     Bob   30   60000
# 2 Charlie   35   70000

# Each column is a Series
print(type(df['name']))  # <class 'pandas.core.series.Series'>
```

### 3. Index — The Labels

The Index is the "row labels" of a DataFrame. It enables:
- Fast lookups
- Data alignment
- Hierarchical (multi-level) indexing

```python
df = pd.DataFrame(
    {'A': [1, 2, 3], 'B': [4, 5, 6]},
    index=['row1', 'row2', 'row3']
)
print(df.index)  # Index(['row1', 'row2', 'row3'], dtype='object')
```

---

## Creating DataFrames: All Methods

```python
import pandas as pd

# 1. From dictionary (most common)
df1 = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': ['a', 'b', 'c']
})

# 2. From list of lists (with columns)
df2 = pd.DataFrame(
    [[1, 'a'], [2, 'b'], [3, 'c']],
    columns=['col1', 'col2']
)

# 3. From list of dictionaries
df3 = pd.DataFrame([
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 30}
])

# 4. From numpy array
import numpy as np
df4 = pd.DataFrame(
    np.random.randn(4, 3),
    columns=['A', 'B', 'C']
)

# 5. From CSV file (we'll cover in Module 01)
# df5 = pd.read_csv('data.csv')

# 6. From Excel file
# df6 = pd.read_excel('data.xlsx')
```

---

## Essential DataFrame Attributes

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'age': [25, 30, 35, 28],
    'salary': [50000, 60000, 70000, 55000],
    'department': ['Engineering', 'Sales', 'Engineering', 'Marketing']
})

# Shape: (rows, columns)
print(df.shape)  # (4, 4)

# Columns: column names
print(df.columns)  # Index(['name', 'age', 'salary', 'department'], dtype='object')

# Index: row labels
print(df.index)  # RangeIndex(start=0, stop=4, step=1)

# dtypes: data type of each column
print(df.dtypes)
# name         object
# age           int64
# salary        int64
# department   object
# dtype: object

# Values: underlying numpy array
print(df.values)

# T: transpose (swap rows and columns)
print(df.T)

# info(): memory and type summary
print(df.info())

# memory_usage(): how much RAM each column uses
print(df.memory_usage())
```

---

## Setting and Resetting Index

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

# Set a column as index (why? faster lookups, meaningful labels)
df_indexed = df.set_index('name')
print(df_indexed)
#          age  salary
# name
# Alice     25   50000
# Bob       30   60000
# Charlie   35   70000

# Reset index (convert index back to column)
df_reset = df_indexed.reset_index()
print(df_reset)

# Why set an index?
# 1. Faster lookups by label
# 2. Meaningful row identifiers
# 3. Required for time-series operations
# 4. Enables hierarchical indexing
```

---

## Viewing Data

```python
# First N rows
df.head(3)

# Last N rows
df.tail(2)

# Random sample
df.sample(3)              # 3 random rows
df.sample(frac=0.5)       # 50% of rows randomly

# Specific rows by position
df.iloc[0]                # First row
df.iloc[0:3]              # First 3 rows
df.iloc[[0, 2]]           # Rows 0 and 2

# Specific rows by label
df.loc[0]                 # Row with index label 0
df.loc[0:2]               # Rows with labels 0, 1, 2 (inclusive!)
```

**Important:** `loc` is label-based (inclusive of end), `iloc` is position-based (exclusive of end).

---

## Next Steps

- **Module 01:** Learn to load data from CSV, JSON, Excel, SQL, APIs
- **Module 02:** Explore and understand your data (EDA)
- **Module 03:** Clean and prepare messy real-world data

---

## Quick Reference

| Operation | Code | Description |
|-----------|------|-------------|
| Create DataFrame | `pd.DataFrame(dict)` | From dictionary |
| View shape | `df.shape` | (rows, cols) |
| View columns | `df.columns` | Column names |
| View types | `df.dtypes` | Data types |
| First rows | `df.head(n)` | Top n rows |
| Random sample | `df.sample(n)` | Random n rows |
| Set index | `df.set_index('col')` | Use column as index |
| Reset index | `df.reset_index()` | Convert index to column |
| Info | `df.info()` | Structure summary |
| Memory | `df.memory_usage()` | RAM usage |
