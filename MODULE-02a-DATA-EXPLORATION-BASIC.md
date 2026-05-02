# MODULE-02a: DATA EXPLORATION — BASIC EDA

## What is EDA and Why It Matters

**Exploratory Data Analysis (EDA)** is the process of understanding your data before modeling or reporting.

**Why EDA first?**
- Reveals data quality issues (missing values, outliers, errors)
- Uncovers patterns and relationships
- Informs feature engineering decisions
- Prevents garbage-in-garbage-out scenarios

> "The greatest value of a picture is when it forces us to notice what we never expected to see." — John Tukey

---

## Loading Sample Data

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'employee_id': range(1, 101),
    'name': [f'Employee_{i}' for i in range(1, 101)],
    'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'], 100),
    'age': np.random.randint(22, 65, 100),
    'salary': np.random.randint(40000, 150000, 100),
    'years_experience': np.random.randint(0, 40, 100),
    'performance_score': np.round(np.random.uniform(1.0, 5.0, 100), 1),
    'hire_date': pd.date_range('2015-01-01', periods=100, freq='3D'),
    'remote_work': np.random.choice([True, False], 100),
    'city': np.random.choice(['New York', 'London', 'Tokyo', 'Sydney', 'Berlin'], 100)
})

# Add some missing values for realism
df.loc[df.sample(10).index, 'salary'] = np.nan
df.loc[df.sample(5).index, 'performance_score'] = np.nan
```

---

## Step 1: First Look — Shape and Structure

```python
# --- DIMENSIONS ---
print(f"Shape: {df.shape}")          # (rows, columns)
print(f"Rows: {df.shape[0]}")        # Number of records
print(f"Columns: {df.shape[1]}")     # Number of features

# --- COLUMN NAMES ---
print(df.columns.tolist())           # List of column names
print(df.columns)                    # Index object

# --- DATA TYPES ---
print(df.dtypes)
# Why check dtypes?
# - object columns might need conversion to category
# - numeric columns stored as strings need conversion
# - datetime columns need parsing

# --- DETAILED STRUCTURE ---
print(df.info())
# Shows: column names, non-null counts, dtypes, memory usage
# Why? Quick scan for missing data and type issues
```

---

## Step 2: Sample the Data

```python
# --- FIRST ROWS ---
print(df.head())                     # First 5 rows (default)
print(df.head(10))                   # First 10 rows

# --- LAST ROWS ---
print(df.tail())                     # Last 5 rows
# Why check tail? Sometimes data quality issues appear at end

# --- RANDOM SAMPLES ---
print(df.sample(5))                  # 5 random rows
print(df.sample(n=5, random_state=42))  # Reproducible sample
print(df.sample(frac=0.1))           # 10% of data

# --- SPECIFIC ROWS ---
print(df.iloc[0])                    # First row (by position)
print(df.loc[0])                     # Row with index label 0
```

---

## Step 3: Numerical Summary Statistics

```python
# --- BASIC DESCRIPTION ---
print(df.describe())
# Shows: count, mean, std, min, 25%, 50%, 75%, max
# Why? Quick overview of distribution and potential outliers

# --- INCLUDE ALL COLUMNS ---
print(df.describe(include='all'))
# For object columns: shows count, unique, top (most frequent), freq

# --- SPECIFIC STATISTICS ---
print(df['salary'].mean())           # Average
print(df['salary'].median())         # Middle value (robust to outliers)
print(df['salary'].mode())           # Most frequent value
print(df['salary'].std())            # Standard deviation (spread)
print(df['salary'].min())            # Minimum
print(df['salary'].max())            # Maximum
print(df['salary'].quantile(0.90))   # 90th percentile
print(df['salary'].quantile([0.25, 0.50, 0.75]))  # Quartiles

# --- WHY MEAN VS MEDIAN? ---
# Mean is sensitive to outliers; median is robust
# Use median when data is skewed (income, house prices, etc.)
```

---

## Step 4: Categorical Data Analysis

```python
# --- VALUE COUNTS ---
print(df['department'].value_counts())
# Why? Understand class distribution, spot imbalances

# --- WITH PERCENTAGES ---
print(df['department'].value_counts(normalize=True) * 100)
# Shows percentage of each category

# --- SORTED BY FREQUENCY ---
print(df['department'].value_counts().sort_index())
# Sort alphabetically instead of by frequency

# --- BINARY COLUMNS ---
print(df['remote_work'].value_counts())
# Quick check of True/False distribution

# --- UNIQUE VALUES ---
print(df['department'].nunique())    # Number of unique values
print(df['department'].unique())     # List of unique values

# --- CROSS-TABULATION ---
print(pd.crosstab(df['department'], df['remote_work']))
# Why? See relationships between two categorical variables
```

---

## Step 5: Missing Data Analysis

```python
# --- COUNT MISSING VALUES ---
print(df.isnull().sum())             # Missing values per column
print(df.isnull().sum().sum())       # Total missing values

# --- PERCENTAGE MISSING ---
missing_pct = df.isnull().mean() * 100
print(missing_pct[missing_pct > 0])  # Only columns with missing data

# --- ROWS WITH ANY MISSING ---
print(df[df.isnull().any(axis=1)])   # Show rows with any NaN

# --- PATTERNS OF MISSINGNESS ---
# Why analyze patterns?
# - MCAR (Missing Completely At Random): no pattern
# - MAR (Missing At Random): depends on observed data
# - MNAR (Missing Not At Random): depends on unobserved data
```

---

## Step 6: Quick Visual EDA

```python
import matplotlib.pyplot as plt

# --- HISTOGRAM ---
df['salary'].hist(bins=30, edgecolor='black')
plt.title('Salary Distribution')
plt.xlabel('Salary')
plt.ylabel('Count')
plt.savefig('charts/eda_salary_hist.png', dpi=150, bbox_inches='tight')
plt.close()

# --- BOX PLOT BY CATEGORY ---
df.boxplot(column='salary', by='department', figsize=(10, 6))
plt.title('Salary by Department')
plt.suptitle('')
plt.ylabel('Salary')
plt.savefig('charts/eda_salary_by_dept.png', dpi=150, bbox_inches='tight')
plt.close()

# --- SCATTER PLOT ---
plt.scatter(df['years_experience'], df['salary'], alpha=0.6)
plt.title('Experience vs Salary')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.savefig('charts/eda_experience_vs_salary.png', dpi=150, bbox_inches='tight')
plt.close()
```

---

## Quick Reference

| Task | Code |
|------|------|
| Shape | `df.shape` |
| First rows | `df.head(n)` |
| Random sample | `df.sample(n)` |
| Column types | `df.dtypes` |
| Structure info | `df.info()` |
| Numerical summary | `df.describe()` |
| All columns summary | `df.describe(include='all')` |
| Value counts | `df['col'].value_counts()` |
| Missing count | `df.isnull().sum()` |
| Missing % | `df.isnull().mean() * 100` |
| Duplicates | `df.duplicated().sum()` |

---

## Next Steps

- **Module 02b:** Advanced EDA (correlation, distributions, EDA function)
- **Module 03a:** Missing values — detection and imputation

