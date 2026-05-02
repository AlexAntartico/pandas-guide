# MODULE-05b: DATA TRANSFORMATION — STRINGS, DATETIME, TIME SERIES

---

## 3. String Operations

The `.str` accessor provides vectorized string methods.

```python
# Sample data with messy strings
df_str = pd.DataFrame({
    'name': ['  Alice Smith ', 'BOB JONES', 'charlie brown ', '  Diana Prince'],
    'email': ['ALICE@EXAMPLE.COM', 'bob@example.com', 'CHARLIE@Example.COM', 'diana@example.com'],
    'phone': ['(555) 123-4567', '555-987-6543', '(555) 456-7890', '555.321.6543']
})

# --- BASIC STRING METHODS ---
df_str['name_clean'] = df_str['name'].str.strip()           # Remove whitespace
df_str['name_lower'] = df_str['name'].str.lower()           # Lowercase
df_str['name_upper'] = df_str['name'].str.upper()           # Uppercase
df_str['name_title'] = df_str['name'].str.title()           # Title Case

# --- EXTRACTION ---
df_str['first_name'] = df_str['name_clean'].str.split().str[0]
df_str['last_name'] = df_str['name_clean'].str.split().str[-1]
df_str['email_domain'] = df_str['email'].str.extract(r'@(.+)$')
df_str['area_code'] = df_str['phone'].str.extract(r'[\(\-](\d{3})[\)\-\.]')

# --- REPLACEMENT ---
df_str['phone_clean'] = df_str['phone'].str.replace(r'[()\-\.\s]', '', regex=True)

# --- PATTERN MATCHING ---
print(df_str['email'].str.contains(r'@example\.com'))  # Contains pattern
print(df_str['email'].str.match(r'^[A-Z]'))            # Starts with uppercase

# --- SPLITTING ---
df_str[['first', 'last']] = df_str['name_clean'].str.split(' ', n=1, expand=True)
# n=1: Split only on first space
# expand=True: Return DataFrame instead of Series of lists

# --- LENGTH AND COUNT ---
df_str['name_length'] = df_str['name_clean'].str.len()
df_str['word_count'] = df_str['name_clean'].str.count(' ') + 1
```

> **JupyterLab:** After building multiple string columns, view a focused before/after subset as the last line in a cell: `df_str[['name', 'name_clean', 'first_name', 'last_name']]` — much easier to read than the full wide DataFrame.

---

## 4. DateTime Operations

```python
# --- PARSING DATES ---
dates = pd.DataFrame({
    'date_str': ['2024-01-15', '01/20/2024', '2024-02-10', '15-Mar-2024'],
    'timestamp': ['2024-01-15 14:30:00', '2024-01-20 09:15:00', '2024-02-10 16:45:00', '2024-03-15 11:00:00']
})

dates['date'] = pd.to_datetime(dates['date_str'])
dates['timestamp'] = pd.to_datetime(dates['timestamp'])
# pd.to_datetime: Auto-detects most date formats
# format='%Y-%m-%d': Specify format for speed and accuracy

# --- EXTRACTING COMPONENTS ---
dates['year'] = dates['date'].dt.year
dates['month'] = dates['date'].dt.month
dates['day'] = dates['date'].dt.day
dates['day_of_week'] = dates['date'].dt.dayofweek      # 0=Monday, 6=Sunday
dates['day_name'] = dates['date'].dt.day_name()        # 'Monday', 'Tuesday', ...
dates['month_name'] = dates['date'].dt.month_name()    # 'January', 'February', ...
dates['quarter'] = dates['date'].dt.quarter             # 1, 2, 3, 4
dates['is_month_start'] = dates['date'].dt.is_month_start
dates['is_month_end'] = dates['date'].dt.is_month_end

# --- DATE ARITHMETIC ---
dates['days_since_epoch'] = (dates['date'] - pd.Timestamp('2024-01-01')).dt.days
dates['next_month'] = dates['date'] + pd.DateOffset(months=1)
dates['age'] = (pd.Timestamp.now() - dates['date']).dt.days / 365.25

# --- DATE RANGES ---
date_range = pd.date_range('2024-01-01', '2024-12-31', freq='D')
# freq='D': Daily, 'W': Weekly, 'M': Month-end, 'Q': Quarter-end, 'Y': Year-end
# freq='B': Business days, 'H': Hours, 'T' or 'min': Minutes

# --- BUSINESS DAYS ---
bday_range = pd.bdate_range('2024-01-01', periods=10)
# Business days only (excludes weekends)
```

---

## 5. Time Series Resampling

```python
# --- CREATE TIME SERIES ---
np.random.seed(42)
ts = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=365, freq='D'),
    'sales': np.random.randint(100, 1000, 365).cumsum()
}).set_index('date')

# --- RESAMPLING ---
# Downsample: Daily → Monthly
monthly = ts['sales'].resample('ME').sum()
# 'ME': Month end (pandas 2.2+)
# aggfunc: sum(), mean(), first(), last(), ohlc()

# Downsample: Daily → Weekly
weekly = ts['sales'].resample('W').mean()

# Upsample: Monthly → Daily (with interpolation)
daily_from_monthly = monthly.resample('D').interpolate()
# Why interpolate? Fill gaps when upsampling

# --- ROLLING WINDOWS ---
# Moving average (smooth out noise)
ts['sales_7d_avg'] = ts['sales'].rolling(window=7).mean()
ts['sales_30d_avg'] = ts['sales'].rolling(window=30).mean()

# Rolling statistics
ts['sales_7d_std'] = ts['sales'].rolling(window=7).std()
ts['sales_7d_min'] = ts['sales'].rolling(window=7).min()
ts['sales_7d_max'] = ts['sales'].rolling(window=7).max()
```

> **JupyterLab:** For a quick visual check, pandas' built-in `.plot()` renders inline with `%matplotlib inline` — no full matplotlib setup needed: `ts[['sales', 'sales_7d_avg', 'sales_30d_avg']].plot(figsize=(12, 4))`.

```python
# --- EXPANDING WINDOWS ---
# Cumulative statistics
ts['cumsum'] = ts['sales'].expanding().sum()
ts['cummean'] = ts['sales'].expanding().mean()
ts['cummax'] = ts['sales'].expanding().max()

# --- EXPONENTIAL WEIGHTED ---
# More weight to recent observations
ts['ewm_30'] = ts['sales'].ewm(span=30).mean()
# Why EWM? React faster to recent changes than simple moving average
```

---

## 6. Categorical Data

```python
# --- CREATE CATEGORIES ---
df_cat = pd.DataFrame({
    'size': ['S', 'M', 'L', 'XL', 'S', 'M', 'L', 'XL'],
    'priority': ['High', 'Low', 'Medium', 'High', 'Low', 'Medium', 'High', 'Low']
})

# Convert to categorical
df_cat['size'] = df_cat['size'].astype('category')

# --- ORDERED CATEGORIES ---
size_order = pd.CategoricalDtype(categories=['S', 'M', 'L', 'XL'], ordered=True)
df_cat['size'] = df_cat['size'].astype(size_order)

priority_order = pd.CategoricalDtype(categories=['Low', 'Medium', 'High'], ordered=True)
df_cat['priority'] = df_cat['priority'].astype(priority_order)

# Why ordered? Enables meaningful sorting and comparison
print(df_cat.sort_values('size'))  # Sorts by category order, not alphabetically

# --- CATEGORY OPERATIONS ---
print(df_cat['size'].cat.categories)    # List categories
print(df_cat['size'].cat.codes)         # Numeric codes (0, 1, 2, ...)

# --- MEMORY SAVINGS ---
df_large = pd.DataFrame({'col': np.random.choice(['A', 'B', 'C', 'D', 'E'], 1_000_000)})
print(f"Object: {df_large['col'].memory_usage(deep=True)} bytes")
df_large['col_cat'] = df_large['col'].astype('category')
print(f"Category: {df_large['col_cat'].memory_usage(deep=True)} bytes")
# Category typically uses ~10-20% of object memory
```

---

## Quick Reference

| Task | Code |
|------|------|
| String strip | `df['col'].str.strip()` |
| String extract | `df['col'].str.extract(r'pattern')` |
| Parse dates | `pd.to_datetime(df['col'])` |
| Date components | `df['col'].dt.year`, `.dt.month`, `.dt.day` |
| Resample | `df.resample('M').sum()` |
| Rolling mean | `df['col'].rolling(7).mean()` |
| Categorical | `df['col'].astype('category')` |

---

## Next Steps

- **Module 06a:** Basic visualization
- **Module 07a:** Export to CSV and Excel

