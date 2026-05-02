# MODULE-04b: DATA MANIPULATION — GROUPBY, MERGE, CONCAT

---

## 5. GroupBy — Split-Apply-Combine

The GroupBy pattern is the most powerful pandas operation.

### The Three Steps

```
1. SPLIT: Divide data into groups based on some key
2. APPLY: Apply a function to each group independently
3. COMBINE: Combine results into a single DataFrame
```

### Basic GroupBy

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
    'age': [25, 30, 35, 28, 32, 40],
    'salary': [50000, 60000, 70000, 55000, 65000, 80000],
    'department': ['Eng', 'Sales', 'Eng', 'HR', 'Sales', 'Eng']
})

# --- AGGREGATION ---
df.groupby('department')['salary'].mean()
df.groupby('department')['salary'].agg(['mean', 'median', 'std', 'min', 'max', 'count'])

# Multiple aggregations per column
df.groupby('department').agg({
    'salary': ['mean', 'median', 'std', 'min', 'max'],
    'age': ['mean', 'min', 'max'],
    'name': 'count'
})

# --- WHY AGGREGATION? ---
# Summarize data by categories
# Compare groups
# Create summary reports
```

> **JupyterLab:** Multi-column `.agg()` creates MultiIndex columns that display as nested headers — readable but awkward to work with. Append `.reset_index()` to flatten to a plain DataFrame that renders cleanly as a table. For single-column agg, the result is already a clean Series or DataFrame.

```python
```

### Transform and Filter

```python
# --- TRANSFORM ---
# Apply function and return result with same index as input
df['dept_avg_salary'] = df.groupby('department')['salary'].transform('mean')
df['salary_diff_from_dept'] = df['salary'] - df['dept_avg_salary']
# Why transform? Keep original row structure while adding group-level info

# --- FILTER ---
# Keep only groups that meet a condition
df.groupby('department').filter(lambda x: len(x) >= 2)
# Why filter? Remove small groups, focus on significant segments

# --- APPLY (complex) ---
# Apply arbitrary function to each group
def normalize_salary(group):
    group['salary_normalized'] = (group['salary'] - group['salary'].mean()) / group['salary'].std()
    return group

df_normalized = df.groupby('department').apply(normalize_salary)
# Why apply? Complex operations that don't fit agg/transform
```

### Advanced GroupBy Patterns

```python
# --- MULTIPLE GROUPING COLUMNS ---
df.groupby(['department'])['salary'].mean()
# Creates MultiIndex (hierarchical index)

# --- NUNIQUE ---
df.groupby('department')['name'].nunique()
# Count unique values per group

# --- CUSTOM AGGREGATION ---
def range_func(x):
    return x.max() - x.min()

df.groupby('department')['salary'].agg(range_func)

# --- SIZE AND COUNT ---
df.groupby('department').size()     # Row count per group (includes NaN)
df.groupby('department').count()    # Non-null count per column
```

---

## 6. Merge and Join

### Types of Joins

```
INNER JOIN: Only matching rows from both tables
LEFT JOIN:  All rows from left, matching from right (NULL if no match)
RIGHT JOIN: All rows from right, matching from left (NULL if no match)
OUTER JOIN: All rows from both tables (NULL where no match)
```

```python
# --- SAMPLE DATA ---
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'dept_id': [101, 102, 101, 103, 102]
})

departments = pd.DataFrame({
    'dept_id': [101, 102, 103, 104],
    'dept_name': ['Engineering', 'Sales', 'HR', 'Marketing']
})

# --- INNER JOIN (default) ---
merged = pd.merge(employees, departments, on='dept_id')

# --- LEFT JOIN ---
merged = pd.merge(employees, departments, on='dept_id', how='left')

# --- RIGHT JOIN ---
merged = pd.merge(employees, departments, on='dept_id', how='right')

# --- OUTER JOIN ---
merged = pd.merge(employees, departments, on='dept_id', how='outer')

# --- JOIN ON DIFFERENT COLUMN NAMES ---
pd.merge(employees, departments, left_on='dept_id', right_on='dept_id')

# --- WHY MERGE vs JOIN? ---
# merge(): More flexible, explicit join type, works on any columns
# join(): Simpler syntax, joins on index by default
```

### Merge Indicators

```python
# Track which table each row came from
merged = pd.merge(employees, departments, on='dept_id', how='outer', indicator=True)
print(merged['_merge'])
# Values: 'left_only', 'right_only', 'both'
# Why indicator? Debug join issues, understand data overlap
```

> **JupyterLab:** After a merge, place `merged['_merge'].value_counts()` as the last line in a cell — it renders as a Series table and immediately shows how many rows matched vs. came from only one side, without scrolling through the full result.

---

## 7. Concat and Append

```python
# --- VERTICAL CONCATENATION (stacking rows) ---
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

result = pd.concat([df1, df2], ignore_index=True)
# ignore_index=True: Reset index in result
# Why concat? Combine datasets with same columns

# --- HORIZONTAL CONCATENATION (stacking columns) ---
df3 = pd.DataFrame({'C': [9, 10], 'D': [11, 12]})
result = pd.concat([df1, df3], axis=1)
# axis=1: Concatenate along columns
# Why horizontal concat? Add new columns from another source
```

---

## Quick Reference

| Task | Code |
|------|------|
| Group and aggregate | `df.groupby('col').agg({'val': 'mean'})` |
| Transform | `df.groupby('col')['val'].transform('mean')` |
| Filter groups | `df.groupby('col').filter(lambda x: len(x) > 2)` |
| Merge tables | `pd.merge(df1, df2, on='key')` |
| Left join | `pd.merge(df1, df2, on='key', how='left')` |
| Concatenate | `pd.concat([df1, df2])` |

---

## Next Steps

- **Module 05a:** Pivot tables and reshaping
- **Module 06a:** Basic visualization

