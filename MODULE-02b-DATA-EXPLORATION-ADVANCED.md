# MODULE-02b: DATA EXPLORATION — ADVANCED EDA

---

## Step 7: Correlation Analysis

```python
import numpy as np

# --- NUMERICAL CORRELATION ---
correlation = df.select_dtypes(include=[np.number]).corr()
print(correlation)
# Why? Identify relationships between numerical variables
# Values: -1 (perfect negative) to +1 (perfect positive)

# --- CORRELATION WITH TARGET ---
# If you have a target variable:
print(correlation['salary'].sort_values(ascending=False))
# Which features correlate most with salary?

# --- STRONG CORRELATIONS ---
# Find highly correlated pairs (potential multicollinearity)
def find_high_correlations(df, threshold=0.7):
    corr = df.corr()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    return upper.stack().sort_values(ascending=False)

print(find_high_correlations(df, threshold=0.3))

# --- SPEARMAN CORRELATION ---
# For non-linear relationships or ordinal data
print(df.select_dtypes(include=[np.number]).corr(method='spearman'))
```

---

## Step 8: Distribution Analysis

```python
# --- HISTOGRAM DATA ---
print(df['salary'].value_counts(bins=10).sort_index())
# Bin numerical data into 10 ranges

# --- SKEWNESS ---
print(df['salary'].skew())
# Why? Skewness tells you if distribution is asymmetric
# Positive skew: tail on right (most values low, few very high)
# Negative skew: tail on left (most values high, few very low)
# ~0: symmetric distribution

# --- KURTOSIS ---
print(df['salary'].kurt())
# Why? Kurtosis tells you about tail heaviness
# High kurtosis: heavy tails (more outliers)
# Low kurtosis: light tails (fewer outliers)

# --- GROUPED STATISTICS ---
print(df.groupby('department')['salary'].agg(['mean', 'median', 'std', 'count']))
# Why? Compare distributions across categories
```

---

## Step 9: Correlation Heatmap

```python
import matplotlib.pyplot as plt
import seaborn as sns

# --- CORRELATION HEATMAP ---
plt.figure(figsize=(10, 8))
sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.savefig('charts/eda_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
```

> **JupyterLab:** With `%matplotlib inline` active, `plt.close()` suppresses the inline display — swap it for `plt.show()` (or remove it) to see the heatmap in the notebook. Keep `plt.savefig()` before `plt.show()` if you want both inline display and a saved file.

---

## Step 10: Production EDA Function

```python
def quick_eda(df, target_col=None):
    """
    Production-grade quick EDA function.
    Run this on any new dataset.
    """
    print("=" * 60)
    print("QUICK EDA REPORT")
    print("=" * 60)
    
    # 1. Shape
    print(f"\n📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # 2. Types
    print(f"\n📋 Data Types:")
    print(df.dtypes.value_counts())
    
    # 3. Missing data
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    print(f"\n❌ Missing Data:")
    for col in df.columns:
        if missing[col] > 0:
            print(f"  {col}: {missing[col]} ({missing_pct[col]:.1f}%)")
    
    # 4. Duplicates
    dupes = df.duplicated().sum()
    print(f"\n🔄 Duplicates: {dupes} ({dupes/len(df)*100:.1f}%)")
    
    # 5. Numerical summary
    print(f"\n📈 Numerical Columns:")
    print(df.select_dtypes(include=[np.number]).describe())
    
    # 6. Categorical summary
    print(f"\n📝 Categorical Columns:")
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        print(f"\n  {col}:")
        print(f"    Unique: {df[col].nunique()}")
        print(f"    Top 3: {df[col].value_counts().head(3).to_dict()}")
    
    # 7. Correlations (if target specified)
    if target_col:
        print(f"\n🎯 Correlations with '{target_col}':")
        num_cols = df.select_dtypes(include=[np.number]).columns
        corr = df[num_cols].corr()[target_col].sort_values(ascending=False)
        print(corr)
    
    print("\n" + "=" * 60)

# Usage
quick_eda(df, target_col='salary')
```

> **JupyterLab:** `quick_eda()` uses `print()` throughout, which works fine in Jupyter. For richer output, replace the `df.describe()` print with `display(df.select_dtypes(include=[np.number]).describe())` — it renders as a styled HTML table instead of plain text.

---

## Quick Reference

| Task | Code |
|------|------|
| Correlation | `df.corr()` |
| Skewness | `df['col'].skew()` |
| Grouped stats | `df.groupby('col')['val'].agg(['mean', 'std'])` |
| Heatmap | `sns.heatmap(df.corr(), annot=True)` |
| Full EDA | `quick_eda(df, target_col='salary')` |

---

## Next Steps

- **Module 03a:** Missing values — detection and imputation
- **Module 06a:** Basic visualization (line, bar, scatter)

