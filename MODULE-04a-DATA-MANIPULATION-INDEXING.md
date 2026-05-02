# MODULE-04a: DATA MANIPULATION — INDEXING, FILTERING, SORTING

---

## 1. Indexing and Selection

### The Four Accessors

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'age': [25, 30, 35, 28, 32],
    'salary': [50000, 60000, 70000, 55000, 65000],
    'department': ['Eng', 'Sales', 'Eng', 'HR', 'Sales']
}, index=['a', 'b', 'c', 'd', 'e'])

# --- loc: LABEL-based ---
# Syntax: df.loc[row_labels, column_labels]
print(df.loc['a'])                    # Row 'a' (all columns)
print(df.loc['a', 'name'])            # Single value
print(df.loc['a':'c'])                # Slice (inclusive of 'c'!)
print(df.loc[['a', 'c'], ['name', 'salary']])  # Specific rows and columns
print(df.loc[df['age'] > 28])         # Boolean filter by label

# --- iloc: POSITION-based ---
# Syntax: df.iloc[row_positions, column_positions]
print(df.iloc[0])                     # First row
print(df.iloc[0, 0])                  # First value (row 0, col 0)
print(df.iloc[0:3])                   # First 3 rows (exclusive of 3)
print(df.iloc[[0, 2], [0, 2]])        # Rows 0,2 and cols 0,2
print(df.iloc[:, 1:3])                # All rows, columns 1-2

# --- at: LABEL-based (single value, faster) ---
print(df.at['a', 'name'])             # Faster than loc for single value

# --- iat: POSITION-based (single value, faster) ---
print(df.iat[0, 0])                   # Faster than iloc for single value

# WHY FOUR ACCESSORS?
# loc/iloc: Flexible, support slices and lists
# at/iat: Fast, single value only (optimization)
```

### Common Indexing Patterns

```python
# --- SELECT SINGLE COLUMN ---
df['name']            # Returns Series
df[['name']]          # Returns DataFrame (note double brackets)
df.name               # Attribute access (only works if valid Python identifier)

# --- SELECT MULTIPLE COLUMNS ---
df[['name', 'salary']]

# --- SELECT ROWS BY CONDITION ---
df[df['age'] > 28]
df[(df['age'] > 28) & (df['department'] == 'Eng')]  # Multiple conditions
df[(df['age'] > 28) | (df['department'] == 'HR')]   # OR condition

# --- QUERY METHOD (cleaner syntax) ---
df.query('age > 28 and department == "Eng"')
df.query('age > 28 or department == "HR"')
# Why query()? More readable, no need for & | operators
```

> **JupyterLab:** Reference notebook variables inside `query()` using `@`: `threshold = 28; df.query('age > @threshold')`. This lets you define filter parameters in one cell and reuse them across queries without rewriting strings.

```python
# --- ISIN for multiple values ---
df[df['department'].isin(['Eng', 'Sales'])]
df[~df['department'].isin(['HR'])]  # NOT in list (~ negates)

# --- BETWEEN ---
df[df['age'].between(28, 35)]
# Equivalent to: (df['age'] >= 28) & (df['age'] <= 35)

# --- STR accessor for string filtering ---
df[df['name'].str.startswith('A')]
df[df['name'].str.contains('li')]
```

---

## 2. Sorting

```python
# --- SORT BY SINGLE COLUMN ---
df.sort_values('salary')              # Ascending (default)
df.sort_values('salary', ascending=False)  # Descending

# --- SORT BY MULTIPLE COLUMNS ---
df.sort_values(['department', 'salary'], ascending=[True, False])
# Sort by department (A-Z), then salary (high-low) within each department

# --- SORT BY INDEX ---
df.sort_index()                       # Sort rows by index
df.sort_index(axis=1)                 # Sort columns by name

# --- IN-PLACE SORTING ---
df.sort_values('salary', inplace=True)
# Why inplace? Saves memory (no copy), but modifies original
```

---

## 3. Column Operations

```python
# --- ADD NEW COLUMN ---
df['bonus'] = df['salary'] * 0.10
df['age_group'] = pd.cut(df['age'], bins=[20, 30, 40, 50], labels=['20s', '30s', '40s'])
# pd.cut: discretize continuous data into bins
# Why cut? Create categories for analysis (age groups, salary bands)

df['salary_k'] = df['salary'] / 1000
df['is_senior'] = df['age'] > 30

# --- ASSIGN METHOD (chaining) ---
df = df.assign(
    bonus=lambda x: x['salary'] * 0.10,
    salary_k=lambda x: x['salary'] / 1000
)
# Why assign()? Enables method chaining, functional style
```

> **JupyterLab:** `assign()` is ideal for Jupyter exploration — chain transforms and filters in one cell without intermediate variables: `(df.assign(bonus=lambda x: x['salary'] * 0.10).query('bonus > 6000'))`. Place the result as the last expression to get an HTML table.

```python
# --- DROP COLUMNS ---
df = df.drop(columns=['bonus'])
df.drop(columns=['bonus'], inplace=True)
df = df[['name', 'age', 'salary']]  # Select only specific columns

# --- RENAME COLUMNS ---
df = df.rename(columns={'name': 'employee_name', 'salary': 'annual_salary'})
# Why rename? Standardize column names, fix typos

# --- REORDER COLUMNS ---
df = df[['department', 'name', 'age', 'salary']]
# Why reorder? Logical grouping, presentation order

# --- INSERT COLUMN AT SPECIFIC POSITION ---
df.insert(1, 'employee_id', range(1, len(df)+1))
# insert(loc, column, value) — inserts at position `loc`
```

---

## 4. Apply Functions

```python
# --- apply: row/column-wise operations ---
df.apply(lambda x: x.mean())  # Mean of each numeric column
df.apply(lambda row: row['salary'] * 1.10, axis=1)  # Apply to each row
# Why axis=1? When you need values from multiple columns

# --- applymap: element-wise operations ---
df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# --- map: element-wise on Series ---
df['department'].map({'Eng': 'Engineering', 'Sales': 'Sales', 'HR': 'Human Resources'})
# Why map? Replace values using dict or Series (faster than apply for single column)

# --- WHEN TO USE WHAT? ---
# map(): Single column, value replacement (fastest)
# applymap(): All cells, same function (medium)
# apply(): Rows or columns, complex logic (slowest)
# Vectorized operations: Always prefer when possible (fastest)
```

---

## Quick Reference

| Task | Code |
|------|------|
| Label-based selection | `df.loc[row, col]` |
| Position-based selection | `df.iloc[row, col]` |
| Boolean filter | `df[df['col'] > 0]` |
| Query method | `df.query('col > 0')` |
| Multiple conditions | `df[(cond1) & (cond2)]` |
| Sort by column | `df.sort_values('col')` |
| Add column | `df['new'] = ...` |
| Drop column | `df.drop(columns=['col'])` |
| Rename column | `df.rename(columns={'old': 'new'})` |
| Apply function | `df.apply(func, axis=1)` |

---

## Next Steps

- **Module 04b:** GroupBy, merge, and concat
- **Module 05a:** Pivot tables and reshaping

