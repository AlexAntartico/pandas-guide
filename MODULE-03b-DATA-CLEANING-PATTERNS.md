# MODULE-03b: DATA CLEANING — DUPLICATES, TYPES, STRINGS, OUTLIERS

---

## 3. Duplicate Detection and Removal

> **JupyterLab:** Same cell re-execution caution as Module 03a: use `df_clean = df.copy()` and apply all mutations to `df_clean`. This keeps your original `df` intact so re-running any cell doesn't produce unexpected cumulative state.

```python
# --- DETECT DUPLICATES ---
print(df.duplicated())              # Boolean series (True if duplicate)
print(df.duplicated().sum())        # Count of duplicate rows
print(df[df.duplicated(keep=False)])  # Show all duplicates (including first occurrence)

# --- REMOVE DUPLICATES ---
df_clean = df.drop_duplicates()
                        # Remove exact duplicate rows
df_clean = df.drop_duplicates(subset=['email'])
                        # Remove duplicates based on specific column
df_clean = df.drop_duplicates(subset=['name', 'email'], keep='last')
                        # Keep last occurrence

# Why keep='first' vs 'last'?
# 'first': Keep original record, remove later entries
# 'last': Keep most recent record (useful for updated data)
```

---

## 4. Type Conversion and Validation

```python
# --- CHECK CURRENT TYPES ---
print(df.dtypes)

# --- CONVERT TYPES ---
# String to numeric
df['age'] = pd.to_numeric(df['age'], errors='coerce')
                        # errors='coerce': invalid values become NaN
                        # errors='raise': raise exception on invalid
                        # errors='ignore': leave invalid values as-is

# String to datetime
df['hire_date'] = pd.to_datetime(df['hire_date'], format='%Y-%m-%d')

# Numeric to categorical
df['department'] = df['department'].astype('category')
                        # Why category? Saves memory, faster operations
                        # Use when: few unique values relative to row count

# Integer with NaN (pandas nullable integer)
df['age'] = df['age'].astype('Int64')  # Capital I — nullable integer
                        # Why? Standard int64 cannot hold NaN

# --- VALIDATE TYPES ---
def validate_types(df, expected_types):
    """Validate that columns have expected types."""
    issues = []
    for col, expected in expected_types.items():
        actual = str(df[col].dtype)
        if actual != expected:
            issues.append(f"  {col}: expected {expected}, got {actual}")
    if issues:
        print("Type validation issues:")
        for issue in issues:
            print(issue)
    else:
        print("All types valid ✓")

validate_types(df, {
    'age': 'int64',
    'salary': 'float64',
    'department': 'category'
})
```

---

## 5. String Cleaning

```python
# --- COMMON STRING ISSUES ---
df['name'] = df['name'].str.strip()         # Remove leading/trailing whitespace
df['name'] = df['name'].str.lower()         # Convert to lowercase
df['name'] = df['name'].str.upper()         # Convert to uppercase
df['name'] = df['name'].str.title()         # Title case (First Letter Capital)
df['name'] = df['name'].str.replace('  ', ' ')  # Replace double spaces

# --- EXTRACTION ---
# Extract parts of strings
df['domain'] = df['email'].str.extract(r'@(.+)$')
                        # Extract domain from email
df['first_name'] = df['name'].str.split().str[0]
                        # Extract first word
df['last_name'] = df['name'].str.split().str[-1]
                        # Extract last word

# --- PATTERN MATCHING ---
print(df['email'].str.contains(r'@.+\..+'))  # Basic email pattern
print(df['email'].str.match(r'^[a-z]+@'))     # Starts with lowercase letters

# --- REPLACEMENT ---
df['department'] = df['department'].str.replace('Eng', 'Engineering')
df['department'] = df['department'].replace({
    'Eng': 'Engineering',
    'Sales': 'Sales',
    'HR': 'Human Resources'
})

# --- LENGTH AND COUNT ---
print(df['email'].str.len())                 # String length
print(df['email'].str.count('@'))            # Count occurrences of @
```

---

## 6. Outlier Detection and Handling

```python
# --- STATISTICAL OUTLIER DETECTION ---
# IQR Method (Interquartile Range)
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['salary'] < lower_bound) | (df['salary'] > upper_bound)]
print(f"Outliers detected: {len(outliers)}")

# Z-Score Method
from scipy import stats
z_scores = np.abs(stats.zscore(df['salary'].dropna()))
outliers_z = df['salary'].dropna()[z_scores > 3]
print(f"Z-score outliers (>3σ): {len(outliers_z)}")

# --- HANDLE OUTLIERS ---
# Option 1: Cap values (winsorize)
df['salary_capped'] = df['salary'].clip(lower=lower_bound, upper=upper_bound)
# Why cap? Preserves data but limits extreme influence

# Option 2: Remove outliers
df_no_outliers = df[(df['salary'] >= lower_bound) & (df['salary'] <= upper_bound)]

# Option 3: Log transform (for right-skewed data)
df['salary_log'] = np.log1p(df['salary'])
# Why log? Compresses large values, expands small values
# log1p = log(1+x) — handles zeros safely
```

---

## 7. Data Validation Patterns

```python
# --- BUSINESS RULE VALIDATION ---
def validate_data(df):
    """Production-grade data validation."""
    issues = []
    
    # Check for negative ages
    if (df['age'] < 0).any():
        issues.append("Negative ages found")
    
    # Check for future dates
    if (df['hire_date'] > pd.Timestamp.now()).any():
        issues.append("Future hire dates found")
    
    # Check for impossible salaries
    if (df['salary'] < 0).any():
        issues.append("Negative salaries found")
    
    # Check for empty strings in required fields
    if df['name'].str.strip().eq('').any():
        issues.append("Empty names found")
    
    # Check for duplicate IDs
    if df['id'].duplicated().any():
        issues.append("Duplicate IDs found")
    
    return issues

issues = validate_data(df)
if issues:
    print("Validation issues:")
    for issue in issues:
        print(f"  ⚠️ {issue}")
else:
    print("✓ All validations passed")
```

---

## Quick Reference

| Task | Code |
|------|------|
| Remove duplicates | `df.drop_duplicates()` |
| Convert type | `df['col'].astype('float')` |
| String to numeric | `pd.to_numeric(df['col'], errors='coerce')` |
| String to date | `pd.to_datetime(df['col'])` |
| Strip whitespace | `df['col'].str.strip()` |
| Detect outliers (IQR) | `Q1 - 1.5*IQR` to `Q3 + 1.5*IQR` |
| Cap outliers | `df['col'].clip(lower, upper)` |

---

## Next Steps

- **Module 04a:** Indexing and filtering
- **Module 06a:** Basic visualization

