# MODULE-07a: DATA EXPORT — CSV AND EXCEL

## Export Overview

After cleaning and analyzing data, you need to output it. Pandas provides `to_*` methods for each format:

| Function | Format | Best For |
|----------|--------|----------|
| `to_csv()` | CSV | Data exchange, imports into other systems |
| `to_excel()` | Excel | Business reports, sharing with non-technical users |
| `to_json()` | JSON | APIs, web applications, NoSQL |
| `to_sql()` | SQL database | Database storage |
| `to_parquet()` | Parquet | Big data, analytics pipelines |

---

## 1. CSV Export

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000],
    'hire_date': pd.to_datetime(['2020-01-15', '2021-03-20', '2019-11-10'])
})

# --- BASIC EXPORT ---
df.to_csv('output.csv')
                        # Default: comma-separated, includes index and header

# --- CRITICAL PARAMETERS ---
df.to_csv('output.csv',
    index=False,            # Don't write row numbers (almost always False)
    header=True,            # Write column names (default True)
    sep=',',                # Field separator (',' for CSV, '\t' for TSV)
    encoding='utf-8',       # Character encoding
    na_rep='',              # Replace NaN with empty string
    columns=['name', 'age'],  # Export only specific columns
    date_format='%Y-%m-%d', # Format for datetime columns
    float_format='%.2f',    # Format for float columns
    quoting=1,              # 0=MINIMAL, 1=ALL, 2=NONNUMERIC, 3=NONE
)

# --- WHY INDEX=FALSE? ---
# Row numbers are meaningless in exported data
# They cause issues when re-importing
# Almost always set index=False for data exchange

# --- EXPORT TO TSV ---
df.to_csv('output.tsv', sep='\t', index=False)

# --- APPEND TO EXISTING FILE ---
df.to_csv('output.csv', mode='a', header=False, index=False)
# mode='a': Append mode (default is 'w' for write/overwrite)
# header=False: Don't write header again
```

---

## 2. Excel Export — Basic

```python
# --- BASIC EXPORT ---
df.to_excel('output.xlsx', index=False)
                        # Uses openpyxl engine by default

# --- WITH PARAMETERS ---
df.to_excel('output.xlsx',
    index=False,
    sheet_name='Employees',   # Sheet name (default 'Sheet1')
    startrow=0,               # Upper-left cell row (0-based)
    startcol=0,               # Upper-left cell column (0-based)
    columns=['name', 'age', 'salary'],  # Specific columns
    header=['Employee Name', 'Age', 'Annual Salary'],  # Custom header names
    float_format='%.2f',
    date_format='YYYY-MM-DD',
    engine='openpyxl',        # For .xlsx files
    engine='xlsxwriter',      # Alternative engine (more formatting options)
)
```

---

## 3. Excel Export — Professional Reports

### Multi-Sheet Reports

```python
# Create multiple DataFrames
summary = df.groupby('department').agg({
    'salary': ['mean', 'median', 'count'],
    'age': 'mean'
})

details = df[['name', 'department', 'salary', 'age']]

trends = df.set_index('hire_date').resample('ME')['salary'].sum()

# Write to multiple sheets
with pd.ExcelWriter('report.xlsx', engine='openpyxl') as writer:
    summary.to_excel(writer, sheet_name='Summary')
    details.to_excel(writer, sheet_name='Details', index=False)
    trends.to_excel(writer, sheet_name='Monthly Trends')
# Why ExcelWriter? Single file with multiple sheets
# Context manager ensures proper file closure
```

### Styled Excel Reports (openpyxl)

```python
from openpyxl.styles import Font, PatternFill, Alignment

with pd.ExcelWriter('styled_report.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Employees', index=False)

    # Get the workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Employees']

    # --- HEADER STYLING ---
    header_font = Font(bold=True, color='FFFFFF', size=12)
    header_fill = PatternFill(start_color='2563eb', end_color='2563eb', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center')

    for cell in worksheet[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

    # --- DATA STYLING ---
    data_font = Font(size=11)
    for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row,
                                    min_col=1, max_col=worksheet.max_column):
        for cell in row:
            cell.font = data_font
            cell.alignment = Alignment(vertical='center')

    # --- ALTERNATING ROW COLORS ---
    even_fill = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
    for row_num in range(2, worksheet.max_row + 1):
        if row_num % 2 == 0:
            for cell in worksheet[row_num]:
                cell.fill = even_fill

    # --- AUTO-FIT COLUMN WIDTHS ---
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        worksheet.column_dimensions[column].width = max_length + 2

    # --- ADD FILTER ---
    worksheet.auto_filter.ref = worksheet.dimensions

    # --- FREEZE TOP ROW ---
    worksheet.freeze_panes = 'A2'

print("Styled report saved to styled_report.xlsx")
```

### Styled Excel Reports (xlsxwriter)

```python
# xlsxwriter provides more built-in formatting
with pd.ExcelWriter('styled_xlsxwriter.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Employees', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Employees']

    # Define formats
    header_fmt = workbook.add_format({
        'bold': True,
        'font_color': 'FFFFFF',
        'bg_color': '#2563eb',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })

    data_fmt = workbook.add_format({
        'border': 1,
        'align': 'right',
        'num_format': '#,##0.00'
    })

    money_fmt = workbook.add_format({
        'border': 1,
        'num_format': '$#,##0'
    })

    # Apply header format
    for col_num, value in enumerate(df.columns):
        worksheet.write(0, col_num, value, header_fmt)

    # Apply data formats
    for row_num, row_data in enumerate(df.values, start=1):
        for col_num, value in enumerate(row_data):
            if df.columns[col_num] == 'salary':
                worksheet.write(row_num, col_num, value, money_fmt)
            else:
                worksheet.write(row_num, col_num, value, data_fmt)

    # Auto-fit columns
    worksheet.autofit()
    print("xlsxwriter report saved")
```

---

## Quick Reference

| Task | Code |
|------|------|
| Export CSV | `df.to_csv('file.csv', index=False)` |
| Export TSV | `df.to_csv('file.tsv', sep='\t', index=False)` |
| Export Excel | `df.to_excel('file.xlsx', index=False)` |
| Multi-sheet Excel | `pd.ExcelWriter('file.xlsx')` with context manager |
| Append CSV | `df.to_csv('file.csv', mode='a', header=False)` |
| Custom float format | `df.to_csv('file.csv', float_format='%.2f')` |
| Custom date format | `df.to_csv('file.csv', date_format='%Y-%m-%d')` |

---

## Next Steps

- **Module 07b:** Export to JSON, SQL, Parquet
- **Module 08a:** Performance optimization

