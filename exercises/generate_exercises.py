#!/usr/bin/env python3
"""Generate the guided exercise notebooks in exercises/.

Each notebook maps to one module of the guide and walks through the bundled
TechRetail datasets (datasets/raw/) with step-by-step, commented code cells.

Run from the repository root:

    python exercises/generate_exercises.py

The notebooks assume JupyterLab is launched from the repository root, so the
`datasets/raw/...` paths below resolve correctly.
"""

import json
from pathlib import Path

HERE = Path(__file__).parent

KERNELSPEC = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}


def md(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.rstrip("\n").splitlines(keepends=True),
    }


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.rstrip("\n").splitlines(keepends=True),
    }


def write_notebook(name, cells):
    for i, cell in enumerate(cells):
        cell["id"] = f"{name}-cell-{i}"
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": KERNELSPEC,
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    out = HERE / f"{name}.ipynb"
    out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  wrote {out.name}")


# ======================================================================
# 00 — GETTING STARTED
# ======================================================================
NB00 = [
    md("# 00 — Getting Started with pandas\n\n"
       "Maps to **MODULE-00**. You will create `Series`/`DataFrame` objects from "
       "scratch, then load and inspect a real table.\n\n"
       "Data: `datasets/raw/customers.csv`  •  Docs: `datasets/README.md`"),
    code("""import pandas as pd
import numpy as np"""),
    md("### 1. Create a Series from scratch\n\n"
       "A `Series` is a 1-D labeled array (a single spreadsheet column)."),
    code("""s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
s"""),
    code("""# Access by label vs by position
s['a']        # label-based
s.iloc[0]     # position-based"""),
    md("### 2. Create a DataFrame from a dict"),
    code("""df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000],
})
df"""),
    md("### 3. Load a real table and inspect its structure"),
    code("""customers = pd.read_csv('datasets/raw/customers.csv')
customers.shape"""),
    code("""customers.columns.tolist()"""),
    code("""customers.dtypes"""),
    code("""customers.info()   # memory usage + non-null counts"""),
    code("""# Set a column as the index (faster lookups, meaningful labels)
customers_indexed = customers.set_index('customer_id')
customers_indexed.head()"""),
    md("### 4. View the data"),
    code("""customers.head(5)                    # first rows
customers.tail(3)                    # last rows
customers.sample(5, random_state=42)  # random rows"""),
]

# ======================================================================
# 01 — DATA INGESTION
# ======================================================================
NB01 = [
    md("# 01 — Data Ingestion (CSV, JSON, Parquet, TSV)\n\n"
       "Maps to **MODULE-01a / 01b**. Load the same data from different formats "
       "and compare the results.\n\n"
       "Data: `datasets/raw/`  •  Docs: `datasets/README.md` (Phase 1)"),
    code("""import pandas as pd"""),
    md("### 1. CSV vs JSON — same data, different behaviour"),
    code("""customers_csv = pd.read_csv('datasets/raw/customers.csv')
customers_json = pd.read_json('datasets/raw/customers.json')
customers_csv.shape, customers_json.shape"""),
    code("""# Empty fields: CSV reads them as NaN, JSON keeps them as "" (empty string)
print('CSV  NaN count:', customers_csv.isna().sum().sum())
print('JSON ""  count:', (customers_json == '').sum().sum())"""),
    md("### 2. CSV vs Parquet — do dtypes differ?"),
    code("""orders_csv = pd.read_csv('datasets/raw/orders.csv')
orders_parquet = pd.read_parquet('datasets/raw/orders.parquet')

# Parquet preserves the ORIGINAL dtype (strings), CSV re-infers them (float)
orders_csv[['subtotal', 'tax', 'total']].dtypes"""),
    code("""orders_parquet[['subtotal', 'tax', 'total']].dtypes"""),
    md("### 3. Preview a large file without loading it all"),
    code("""pd.read_csv('datasets/raw/orders.csv', nrows=5)"""),
    md("### 4. Parse dates at load time\n\n"
       "Date columns load as strings by default; `parse_dates` fixes that."),
    code("""orders = pd.read_csv('datasets/raw/orders.csv', parse_dates=['order_date'])
orders['order_date'].dtype"""),
    md("### 5. Load flat JSON arrays"),
    code("""reviews = pd.read_json('datasets/raw/reviews.json')
reviews.head()"""),
    md("### 6. Load a TSV (tab-separated) file"),
    code("""promotions = pd.read_csv('datasets/promotions.tsv', sep='\\t')
promotions.head()"""),
    md("### 7. Excel (no file ships here)\n\n"
       "This guide ships no `.xlsx`, but the companion repo "
       "https://github.com/AlexAntartico/pandas_practice loads a multi-sheet workbook "
       "with `pd.read_excel('file.xlsx', sheet_name=None)` → returns a "
       "`{sheet_name: DataFrame}` dict. See MODULE-01b."),
]

# ======================================================================
# 02 — DATA EXPLORATION
# ======================================================================
NB02 = [
    md("# 02 — Data Exploration (EDA)\n\n"
       "Maps to **MODULE-02a / 02b**. Get to know the data before cleaning it.\n\n"
       "Docs: `datasets/README.md` (Phases 1 & 4)  •  `datasets/raw/data_dictionary.md`"),
    code("""import pandas as pd
import numpy as np

orders = pd.read_csv('datasets/raw/orders.csv', parse_dates=['order_date'])
customers = pd.read_csv('datasets/raw/customers.csv')"""),
    md("### 1. First look — shape, columns, types"),
    code("""orders.shape"""),
    code("""orders.dtypes"""),
    md("### 2. Summary statistics"),
    code("""orders.describe()"""),
    code("""# include='all' adds object columns (count, unique, top, freq)
orders.describe(include='all')"""),
    md("### 3. Categorical breakdowns"),
    code("""customers['membership'].value_counts()"""),
    code("""customers['membership'].value_counts(normalize=True).mul(100).round(1)"""),
    code("""orders['status'].value_counts()"""),
    md("### 4. Missing values overview"),
    code("""orders.isnull().sum()"""),
    code("""customers.isnull().sum()"""),
    md("### 5. Correlation between numeric columns"),
    code("""orders.select_dtypes(include='number').corr()"""),
    md("### 6. A reusable quick-EDA function"),
    code("""def quick_eda(df):
    print(f'Shape:       {df.shape}')
    print(f'Missing:     {df.isnull().sum().sum()}')
    print(f'Duplicates:  {df.duplicated().sum()}')
    return df.describe(include='all')

quick_eda(orders)"""),
]

# ======================================================================
# 03 — DATA CLEANING
# ======================================================================
NB03 = [
    md("# 03 — Data Cleaning (missing, duplicates, types, strings, outliers)\n\n"
       "Maps to **MODULE-03a / 03b**. Every issue below is intentional — the full "
       "catalog is in `datasets/DQ-EDGE-CASES.md`.\n\n"
       "Docs: `datasets/README.md` (Phases 2 & 3)"),
    code("""import pandas as pd
import numpy as np

customers = pd.read_csv('datasets/raw/customers.csv')
products = pd.read_csv('datasets/raw/products.csv')
orders = pd.read_csv('datasets/raw/orders.csv', parse_dates=['order_date'])
reviews = pd.read_json('datasets/raw/reviews.json')"""),
    md("### 1. Missing values"),
    code("""# CSV already reads empty fields as NaN
customers.isnull().sum()"""),
    code("""# Where are the missing emails?
customers[customers['email'].isna()][['customer_id', 'first_name', 'email']].head()"""),
    md("### 2. Duplicates — same email, different ID"),
    code("""customers[customers.duplicated('email', keep=False)].sort_values('email').head(20)"""),
    code("""# How many emails appear more than once?
dup_emails = customers['email'].dropna().value_counts()
dup_emails[dup_emails > 1].count()"""),
    md("### 3. Type conversion — parse dates"),
    code("""customers['signup_date'] = pd.to_datetime(customers['signup_date'])
customers['signup_date'].dtype"""),
    md("### 4. Invalid values — future signup dates"),
    code("""future = customers[customers['signup_date'] > pd.Timestamp.now()]
future[['customer_id', 'signup_date']]"""),
    md("### 5. String standardization — states"),
    code("""customers['state'].unique()"""),
    code("""# Map full names back to 2-letter codes
state_map = {'California': 'CA', 'New York': 'NY', 'Texas': 'TX', 'Florida': 'FL'}
customers['state'] = customers['state'].replace(state_map)
customers['state'].unique()"""),
    md("### 6. Normalize product categories"),
    code("""products['category'].unique()"""),
    code("""products['category_clean'] = products['category'].str.replace('_', ' ').str.title()
products['category_clean'].unique()"""),
    md("### 7. Out-of-range values — ratings should be 1–5"),
    code("""reviews['rating'].value_counts().sort_index()"""),
    code("""reviews[~reviews['rating'].between(1, 5)][['review_id', 'product_id', 'rating']]"""),
    md("### 8. A validation function"),
    code("""def validate_orders(df):
    issues = []
    if (df['total'] < 0).any():
        issues.append('negative totals')
    if df['order_date'].max() > pd.Timestamp.now():
        issues.append('future order dates')
    return issues

validate_orders(orders)"""),
]

# ======================================================================
# 04 — DATA MANIPULATION
# ======================================================================
NB04 = [
    md("# 04 — Data Manipulation (indexing, filtering, sorting, groupby, merge)\n\n"
       "Maps to **MODULE-04a / 04b**.\n\n"
       "Docs: `datasets/README.md` (Phases 1, 2 & 5)"),
    code("""import pandas as pd

orders = pd.read_csv('datasets/raw/orders.csv', parse_dates=['order_date'])
customers = pd.read_csv('datasets/raw/customers.csv')"""),
    md("### 1. Indexing — loc vs iloc"),
    code("""orders.iloc[0]            # first row by position
orders.loc[0, 'order_id']  # single value by label"""),
    md("### 2. Boolean filtering"),
    code("""completed = orders[orders['status'] == 'completed']
completed.shape"""),
    code("""# query() for readability
orders.query("status == 'completed' and total > 1000").head()"""),
    code("""# isin() for multiple values
orders[orders['payment_method'].isin(['credit_card', 'paypal'])].shape"""),
    md("### 3. Sorting"),
    code("""orders.sort_values('total', ascending=False).head(10)"""),
    md("### 4. GroupBy — split-apply-combine"),
    code("""orders.groupby('status')['total'].agg(['count', 'sum', 'mean'])"""),
    code("""customers.groupby('membership')['customer_id'].count()"""),
    md("### 5. Merge across tables"),
    code("""order_items = pd.read_csv('datasets/raw/order_items.csv')
products = pd.read_csv('datasets/raw/products.csv')

# orders -> customers -> order_items -> products
merged = (orders
    .merge(customers, on='customer_id')
    .merge(order_items, on='order_id')
    .merge(products, on='product_id'))
merged.shape"""),
    code("""# Revenue by product category
merged.groupby('category')['line_total'].sum().sort_values(ascending=False)"""),
    md("### 6. Concat (stack rows)"),
    code("""pd.concat([orders.head(3), orders.tail(3)])"""),
]

# ======================================================================
# 05 — DATA TRANSFORMATION
# ======================================================================
NB05 = [
    md("# 05 — Data Transformation (pivot, reshape, strings, datetime, time series)\n\n"
       "Maps to **MODULE-05a / 05b**.\n\n"
       "Docs: `datasets/README.md` (Phases 3, 4 & 6)"),
    code("""import pandas as pd

orders = pd.read_csv('datasets/raw/orders.csv', parse_dates=['order_date'])
customers = pd.read_csv('datasets/raw/customers.csv')
order_items = pd.read_csv('datasets/raw/order_items.csv')
products = pd.read_csv('datasets/raw/products.csv')

merged = (orders.merge(customers, on='customer_id')
          .merge(order_items, on='order_id')
          .merge(products, on='product_id'))"""),
    md("### 1. Pivot table — revenue by category × membership"),
    code("""merged.pivot_table(
    values='line_total', index='category', columns='membership',
    aggfunc='sum', fill_value=0)"""),
    md("### 2. Crosstab — count by membership × source"),
    code("""pd.crosstab(customers['membership'], customers['source'])"""),
    md("### 3. Wide → long (melt)"),
    code("""wide = merged.pivot_table(values='line_total', index='category',
                              columns='membership', aggfunc='sum').reset_index()
wide.head()"""),
    code("""long = wide.melt(id_vars='category', var_name='membership', value_name='line_total')
long.head()"""),
    md("### 4. String operations — normalize phone numbers"),
    code("""customers['phone'].head()   # several different formats"""),
    code("""customers['phone_clean'] = customers['phone'].str.replace(r'[^\\d]', '', regex=True)
customers['phone_clean'].head()"""),
    md("### 5. DateTime — extract components"),
    code("""orders['year'] = orders['order_date'].dt.year
orders['month'] = orders['order_date'].dt.month
orders['day_name'] = orders['order_date'].dt.day_name()
orders[['order_date', 'year', 'month', 'day_name']].head()"""),
    md("### 6. Time series — resample & rolling"),
    code("""traffic = pd.read_csv('datasets/raw/website_traffic.csv', parse_dates=['date'])
traffic.set_index('date')['sessions'].resample('ME').sum().head()"""),
    code("""traffic.set_index('date')['sessions'].rolling(7).mean().head(20)"""),
]

# ======================================================================
# 06 — VISUALIZATION
# ======================================================================
NB06 = [
    md("# 06 — Visualization (line, bar, histogram, scatter, box, heatmap)\n\n"
       "Maps to **MODULE-06a / 06b**.\n\n"
       "Docs: `datasets/README.md` (Phases 4 & 7)"),
    code("""%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('deep')

orders = pd.read_csv('datasets/raw/orders.csv', parse_dates=['order_date'])
customers = pd.read_csv('datasets/raw/customers.csv')
order_items = pd.read_csv('datasets/raw/order_items.csv')
products = pd.read_csv('datasets/raw/products.csv')"""),
    md("### 1. Monthly revenue — line chart"),
    code("""monthly = orders.set_index('order_date')['total'].resample('ME').sum()
monthly.plot(figsize=(12, 4), title='Monthly Revenue')"""),
    md("### 2. Revenue by category — bar chart"),
    code("""by_cat = (orders.merge(order_items, on='order_id')
             .merge(products, on='product_id')
             .groupby('category')['line_total'].sum()
             .sort_values())
by_cat.plot(kind='barh', figsize=(10, 6), title='Revenue by Category')"""),
    md("### 3. Order totals — histogram"),
    code("""orders['total'].plot(kind='hist', bins=50, figsize=(10, 5),
                       title='Order Total Distribution')"""),
    md("### 4. Scatter — quantity vs line total"),
    code("""order_items.plot(kind='scatter', x='quantity', y='line_total',
                  alpha=0.3, figsize=(8, 6))"""),
    md("### 5. Box plot — total by membership"),
    code("""sns.boxplot(data=orders.merge(customers, on='customer_id'),
            x='membership', y='total')"""),
    md("### 6. Correlation heatmap"),
    code("""sns.heatmap(orders.select_dtypes(include='number').corr(),
            annot=True, cmap='coolwarm', center=0)"""),
]

# ======================================================================
# 07 — DATA EXPORT
# ======================================================================
NB07 = [
    md("# 07 — Data Export (CSV, Excel, JSON, Parquet, SQL)\n\n"
       "Maps to **MODULE-07a / 07b**.\n\n"
       "Docs: `datasets/README.md` (Phase 7)"),
    code("""import pandas as pd
from pathlib import Path

Path('reports').mkdir(exist_ok=True)

orders = pd.read_csv('datasets/raw/orders.csv', parse_dates=['order_date'])"""),
    md("### 1. Build a summary to export"),
    code("""monthly = orders.set_index('order_date').resample('ME').agg(
    revenue=('total', 'sum'),
    orders=('order_id', 'count'))
monthly.head()"""),
    md("### 2. CSV"),
    code("""monthly.to_csv('reports/monthly_sales.csv', index_label='month')
pd.read_csv('reports/monthly_sales.csv').head()"""),
    md("### 3. Excel — multi-sheet report"),
    code("""by_status = orders.groupby('status')['total'].agg(['count', 'sum'])
with pd.ExcelWriter('reports/sales_report.xlsx', engine='openpyxl') as writer:
    monthly.to_excel(writer, sheet_name='Monthly')
    by_status.to_excel(writer, sheet_name='By Status')
print('wrote reports/sales_report.xlsx')"""),
    md("### 4. JSON"),
    code("""by_status.to_json('reports/by_status.json', orient='records', indent=2)
print('wrote reports/by_status.json')"""),
    md("### 5. Parquet — a fast checkpoint"),
    code("""orders.to_parquet('reports/orders_clean.parquet')
pd.read_parquet('reports/orders_clean.parquet').dtypes   # dtypes preserved"""),
    md("### 6. SQLite"),
    code("""from sqlalchemy import create_engine
engine = create_engine('sqlite:///reports/techretail.db')
orders.to_sql('orders', engine, index=False, if_exists='replace')
pd.read_sql('SELECT status, COUNT(*) AS n FROM orders GROUP BY status', engine)"""),
]

# ======================================================================
# 08 — PRODUCTION / PERFORMANCE
# ======================================================================
NB08 = [
    md("# 08 — Production & Performance (vectorization, memory, chunking, error handling)\n\n"
       "Maps to **MODULE-08a / 08b**.\n\n"
       "Docs: `datasets/README.md` (Phases 3 & 6)"),
    code("""import time
import pandas as pd

orders = pd.read_csv('datasets/raw/orders.csv')"""),
    md("### 1. Vectorization vs loops vs apply"),
    code("""start = time.time()
result = []
for i in range(len(orders)):
    result.append(orders['subtotal'].iloc[i] + orders['tax'].iloc[i])
loop_time = time.time() - start

start = time.time()
orders.apply(lambda r: r['subtotal'] + r['tax'], axis=1)
apply_time = time.time() - start

start = time.time()
orders['subtotal'] + orders['tax']
vec_time = time.time() - start

print(f'loop={loop_time:.4f}s  apply={apply_time:.4f}s  vectorized={vec_time:.4f}s')"""),
    md("### 2. Memory usage & downcasting"),
    code("""orders.memory_usage(deep=True).sum() / 1024  # KB"""),
    code("""def downcast(df):
    for c in df.select_dtypes(include='int64'):
        df[c] = pd.to_numeric(df[c], downcast='integer')
    for c in df.select_dtypes(include='float64'):
        df[c] = pd.to_numeric(df[c], downcast='float')
    return df

orders_opt = downcast(orders.copy())
orders_opt.memory_usage(deep=True).sum() / 1024  # KB"""),
    md("### 3. Categorical for low-cardinality strings"),
    code("""customers = pd.read_csv('datasets/raw/customers.csv')
before = customers['membership'].memory_usage(deep=True)
customers['membership'] = customers['membership'].astype('category')
after = customers['membership'].memory_usage(deep=True)
print(f'membership memory: {before} -> {after} bytes')"""),
    md("### 4. Chunked loading"),
    code("""# For very large files (e.g. datasets/transactions.json, 122 MB — regenerate
# with `python generate_datasets.py`), process in chunks. Demonstrate on orders.csv:
chunks = []
for chunk in pd.read_csv('datasets/raw/orders.csv', chunksize=1000):
    chunks.append(chunk[chunk['status'] == 'completed'])
done = pd.concat(chunks)
done.shape"""),
    md("### 5. Error handling & validation"),
    code("""def safe_load(path):
    from pathlib import Path
    if not Path(path).exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f'{path} is empty')
    return df

safe_load('datasets/raw/orders.csv').shape"""),
    md("### 6. Copy-on-Write"),
    code("""pd.options.mode.copy_on_write = True"""),
]


def main():
    print("Generating exercise notebooks...")
    write_notebook("00_getting_started", NB00)
    write_notebook("01_data_ingestion", NB01)
    write_notebook("02_data_exploration", NB02)
    write_notebook("03_data_cleaning", NB03)
    write_notebook("04_data_manipulation", NB04)
    write_notebook("05_data_transformation", NB05)
    write_notebook("06_visualization", NB06)
    write_notebook("07_data_export", NB07)
    write_notebook("08_production_performance", NB08)


if __name__ == "__main__":
    main()
