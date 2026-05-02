# MODULE-03a: DATA CLEANING — MISSING VALUES

## Why Data Cleaning Matters

Real-world data is messy. Studies show data scientists spend **60-80% of their time** on data cleaning.

---

## 1. Missing Values — Detection and Analysis

```python
import pandas as pd
import numpy as np

# Create messy dataset
df = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'name': ['Alice', 'Bob', None, 'Diana', 'Eve', 'Frank', '', 'Hannah', 'Ivan', 'Jane'],
    'age': [25, 30, np.nan, 35, 28, np.nan, 45, 32, np.nan, 40],
    'salary': [50000, 60000, 55000, np.nan, 70000, 65000, np.nan, 58000, 72000, np.nan],
    'department': ['Eng', 'Sales', 'Eng', 'HR', 'Sales', 'Eng', 'HR', 'Sales', 'Eng', 'HR'],
    'email': ['alice@co.com', 'bob@co.com', 'dan@co.com', None, 'eve@co.com',
              'frank@co.com', 'george@co.com', 'hannah@co.com', 'ivan@co.com', 'jane@co.com']
})

# --- DETECT MISSING VALUES ---
print(df.isnull())           # Boolean DataFrame (True where missing)
# Why isnull() and isna()? They're identical aliases (pandas supports both)

# --- COUNT MISSING ---
print(df.isnull().sum())           # Missing per column
print(df.isnull().sum().sum())     # Total missing

# --- PERCENTAGE MISSING ---
missing_pct = df.isnull().mean() * 100
print(missing_pct)

# --- ROWS WITH ANY MISSING ---
print(df[df.isnull().any(axis=1)])

# --- NON-MISSING COUNT ---
print(df.notnull().sum())          # Non-missing per column
```

---

## 2. Missing Values — Strategies and Imputation

### Strategy Decision Tree

```
Missing Data?
├── <5% missing → Drop rows (if MCAR)
├── 5-20% missing → Impute (mean/median/mode)
├── 20-50% missing → Advanced imputation or flag as separate category
└── >50% missing → Consider dropping column
```

### Drop Missing Values

```python
# --- DROP ROWS ---
df_dropped = df.dropna()
                        # Drop rows with ANY missing value
df_dropped = df.dropna(subset=['salary'])
                        # Drop rows where 'salary' is missing
df_dropped = df.dropna(how='all')
                        # Drop only if ALL values are missing
df_dropped = df.dropna(thresh=3)
                        # Keep rows with at least 3 non-missing values

# --- DROP COLUMNS ---
df_dropped_cols = df.dropna(axis=1)
                        # Drop columns with any missing
df_dropped_cols = df.dropna(axis=1, thresh=int(0.8 * len(df)))
                        # Drop columns with >20% missing

# Why drop vs impute?
# Drop: Simple, but loses data. Only use when missing is minimal and random.
# Impute: Preserves data, but introduces assumptions.
```

### Simple Imputation

```python
# --- NUMERICAL COLUMNS ---
# Mean imputation (use when data is normally distributed)
df['age'] = df['age'].fillna(df['age'].mean())

# Median imputation (use when data is skewed — robust to outliers)
df['salary'] = df['salary'].fillna(df['salary'].median())

# Why mean vs median?
# Mean: sensitive to outliers. Use for symmetric distributions.
# Median: robust to outliers. Use for skewed distributions (income, prices).

# --- CATEGORICAL COLUMNS ---
# Mode imputation (most frequent value)
df['department'] = df['department'].fillna(df['department'].mode()[0])

# --- STRING COLUMNS ---
df['name'] = df['name'].fillna('Unknown')
df['email'] = df['email'].fillna('no-email@company.com')

# --- FORWARD / BACKWARD FILL ---
# For time-series data (fill with previous/next value)
df['salary'] = df['salary'].ffill()  # Forward fill
df['salary'] = df['salary'].bfill()  # Backward fill
# Why? In time series, missing values are often similar to adjacent values
```

### Advanced Imputation

```python
# --- GROUP-BASED IMPUTATION ---
# Fill missing salary with department median
df['salary'] = df.groupby('department')['salary'].transform(
    lambda x: x.fillna(x.median())
)
# Why group-based? Different departments have different salary ranges

# --- INTERPOLATION ---
# Linear interpolation (estimates missing values between known values)
df['age'] = df['age'].interpolate(method='linear')
# Why interpolate? Better than mean for ordered/time-series data

# --- KNN IMPUTATION ---
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=3)
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
# Why KNN? Uses similar rows to estimate missing values
```

---

## Quick Reference

| Task | Code |
|------|------|
| Count missing | `df.isnull().sum()` |
| Drop rows with NaN | `df.dropna()` |
| Fill with mean | `df['col'].fillna(df['col'].mean())` |
| Fill with median | `df['col'].fillna(df['col'].median())` |
| Forward fill | `df['col'].ffill()` |
| Group-based fill | `df.groupby('g')['c'].transform(lambda x: x.fillna(x.median()))` |

---

## Next Steps

- **Module 03b:** Duplicates, type conversion, string cleaning, outliers
- **Module 04a:** Indexing and filtering

