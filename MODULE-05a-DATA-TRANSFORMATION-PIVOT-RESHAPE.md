# MODULE-05a: DATA TRANSFORMATION — PIVOT TABLES AND RESHAPING

---

## 1. Pivot Tables

Pivot tables summarize data by grouping and aggregating — like Excel pivot tables.

```python
import pandas as pd
import numpy as np

# Sample sales data
sales = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100, freq='D'),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'product': np.random.choice(['Widget', 'Gadget', 'Tool'], 100),
    'sales': np.random.randint(100, 1000, 100),
    'quantity': np.random.randint(1, 50, 100),
    'discount': np.random.choice([0, 0.05, 0.10, 0.15, 0.20], 100)
})

# --- BASIC PIVOT TABLE ---
pivot = sales.pivot_table(
    values='sales',           # What to aggregate
    index='region',           # Row groups
    columns='product',        # Column groups
    aggfunc='mean',           # How to aggregate
    fill_value=0              # Fill missing combinations with 0
)
print(pivot)
# Why pivot_table? Create summary reports, compare categories
```

> **JupyterLab:** Pivot tables are among the richest displays in Jupyter — drop `print()` and place `pivot` as the last line in a cell for a styled HTML table. With `margins=True`, the "Total" row/column stands out clearly in the rendered view.

```python

# --- MULTIPLE AGGREGATIONS ---
pivot = sales.pivot_table(
    values=['sales', 'quantity'],
    index='region',
    columns='product',
    aggfunc={'sales': ['mean', 'sum', 'count'], 'quantity': 'sum'},
    fill_value=0,
    margins=True,             # Add row/column totals (Grand Total)
    margins_name='Total'
)
# Why margins? See overall totals alongside breakdowns

# --- PIVOT vs GROUPBY ---
# GroupBy: Returns Series or DataFrame with index
# Pivot table: Returns DataFrame with both row and column indices
# Use pivot_table when you need a cross-tabular report format

# --- CROSSTAB ---
# Special case: frequency count of two categorical variables
ct = pd.crosstab(sales['region'], sales['product'])
print(ct)
# Why crosstab? Quick contingency table, chi-square analysis

# --- CROSSTAB WITH NORMALIZATION ---
ct_pct = pd.crosstab(sales['region'], sales['product'], normalize=True) * 100
print(ct_pct)
# Shows percentage of total
```

---

## 2. Reshaping: Wide ↔ Long

### Wide to Long (Melting)

```python
# Wide format: each month is a column
wide = pd.DataFrame({
    'product': ['A', 'B', 'C'],
    'Jan_2024': [100, 200, 150],
    'Feb_2024': [120, 180, 160],
    'Mar_2024': [110, 210, 140]
})

# --- MELT: Wide → Long ---
long = wide.melt(
    id_vars=['product'],          # Columns to keep as-is
    var_name='month',             # Name for the variable column
    value_name='sales'            # Name for the value column
)
print(long)
# Why melt? Most plotting libraries expect long format
# Long format is better for grouping and filtering
```

> **JupyterLab:** Use `display(wide, long)` in a single cell to show the before/after shape side-by-side — useful for understanding what `melt()` did without switching cells.

```python

# --- STACK: MultiIndex columns → rows ---
df_multi = wide.set_index('product')
stacked = df_multi.stack()
# stack(): Move column level to row index
# unstack(): Move row level to column index
```

### Long to Wide (Pivoting)

```python
# --- PIVOT: Long → Wide ---
wide_back = long.pivot(index='product', columns='month', values='sales')
# Why pivot back? Create comparison tables, export to Excel

# --- PIVOT with aggregation (handles duplicates) ---
wide_agg = long.pivot_table(index='product', columns='month', values='sales', aggfunc='mean')
# Use pivot_table when there might be duplicate (index, column) combinations

# --- UNSTACK: GroupBy result → wide ---
grouped = sales.groupby(['region', 'product'])['sales'].mean()
wide = grouped.unstack()
# unstack(): Move innermost index level to columns
# Why unstack? Create readable reports from grouped data
```

---

## Quick Reference

| Task | Code |
|------|------|
| Pivot table | `df.pivot_table(values='v', index='i', columns='c', aggfunc='mean')` |
| Crosstab | `pd.crosstab(df['a'], df['b'])` |
| Melt (wide→long) | `df.melt(id_vars=['a'], var_name='var', value_name='val')` |
| Pivot (long→wide) | `df.pivot(index='a', columns='b', values='c')` |

---

## Next Steps

- **Module 05b:** String operations, DateTime, time series
- **Module 06a:** Basic visualization

