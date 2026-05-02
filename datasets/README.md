# TechRetail Inc. — Practice Datasets

## Scenario

You are the data analyst at **TechRetail Inc.**, a mid-sized e-commerce company selling electronics, clothing, home goods, books, sports equipment, and beauty products. The company has been operating since 2020 and has accumulated data across multiple systems:

- **CRM** → customer records
- **Order Management** → orders, line items, payments
- **Fulfillment** → shipments and deliveries
- **Product Catalog** → product master data
- **Customer Feedback** → product reviews
- **Marketing** → campaign performance
- **Analytics** → website traffic
- **Customer Service** → returns and refunds

Your job: clean the data, explore it, answer business questions, and produce reports.

---

## File Inventory

```
raw/
├── customers.csv          (~515 rows)  — Customer master
├── customers.json         (~515 rows)  — Same data, JSON format
├── products.csv           (150 rows)   — Product catalog
├── orders.csv             (5,000 rows) — Order transactions
├── orders.parquet         (5,000 rows) — Same data, Parquet format
├── order_items.csv        (~12,000 rows) — Order line items
├── payments.csv           (~5,530 rows) — Payment records
├── payments.json          (~5,530 rows) — Same data, JSON format
├── shipments.csv          (~4,500 rows) — Shipment tracking
├── reviews.json           (2,000 rows) — Product reviews
├── marketing_campaigns.csv (50 rows)   — Campaign performance
├── website_traffic.csv    (~355 rows)   — Daily website metrics
├── returns.csv            (350 rows)   — Return/refund records
└── data_dictionary.md     — Full schema reference

DQ-EDGE-CASES.md           — Catalog of all intentional data quality issues
```

---

## Quick Start

```python
import pandas as pd
import numpy as np

# Load a few tables to begin
customers = pd.read_csv("raw/customers.csv")
products = pd.read_csv("raw/products.csv")
orders = pd.read_csv("raw/orders.csv")
order_items = pd.read_csv("raw/order_items.csv")
```

---

## Exercise Prompts

### Phase 1: Data Loading & Inspection
1. Load all datasets. Compare `customers.csv` vs `customers.json` — do they match?
2. Load `orders.csv` and `orders.parquet` — do dtypes differ?
3. Identify the data types of every column across all tables. Which ones need conversion?
4. Load `reviews.json` — it's a flat JSON array. Convert it to a DataFrame.

### Phase 2: Data Quality Assessment
1. For each table, count missing values per column. Which tables have the most missing data?
2. Identify duplicate customers (same email, different ID). How many?
3. Find orders with invalid status values. What are the unexpected values?
4. Detect orders with negative totals. How many, and what's the total impact?
5. Find products with missing prices. What proportion of the catalog is affected?
6. Identify shipments where delivery_date < ship_date. How many?
7. Find reviews with ratings outside the 1–5 range. What are the values?
8. Detect returns with negative refund amounts. How many?

### Phase 3: Cleaning & Standardization
1. Standardize all state values to 2-letter codes.
2. Normalize product categories to title case.
3. Standardize phone number formats (pick one canonical format).
4. Validate email addresses — flag invalid ones.
5. Normalize order statuses to a consistent set.
6. Fix or flag temporal inconsistencies (future dates, delivery before ship).

### Phase 4: Exploratory Analysis
1. What is the monthly revenue trend? Plot it.
2. Which product categories generate the most revenue?
3. What is the average order value by customer membership tier?
4. Which acquisition channels have the highest conversion rates?
5. What is the distribution of order quantities?
6. Analyze the refund rate by product category.
7. What is the average delivery time by carrier?
8. Correlate marketing spend with conversions.

### Phase 5: Multi-Table Operations
1. Merge orders with customers to get customer details per order.
2. Join order_items with products to get product info per line item.
3. Reconcile payments with orders — find orders with failed payments.
4. Calculate total revenue per customer (orders → order_items → sum).
5. Find customers who have orders but no payments recorded.
6. Calculate return rate by product.
7. Merge website traffic with campaign data — is there a correlation?
8. Build a customer lifetime value table.

### Phase 6: Advanced Analysis
1. Build a cohort analysis: how do customers acquired in different months behave over time?
2. Calculate customer RFM scores (Recency, Frequency, Monetary).
3. Identify products with the highest return rates and lowest ratings.
4. Analyze seasonal patterns in website traffic and sales.
5. Build a marketing attribution model from campaign data.
6. Detect anomalies in daily traffic (spikes, drops).
7. Calculate inventory turnover (if stock data is available).
8. Build a customer segmentation model based on purchase behavior.

### Phase 7: Reporting & Export
1. Create a monthly sales summary report (CSV).
2. Generate a customer analysis report (Excel with multiple sheets).
3. Build a product performance dashboard (pivot table + chart).
4. Export a cleaned version of all tables (CSV + Parquet).
5. Create a data quality summary report.

---

## Reference Files

- **`raw/data_dictionary.md`** — Complete schema reference for all 10 tables
- **`DQ-EDGE-CASES.md`** — Catalog of every intentional data quality issue and what it exercises
