# Data Quality & Edge Cases Reference

This document catalogs every intentional data quality issue and edge case embedded in the datasets. Each entry describes **what exists** and **what it's designed to exercise** — no solutions provided.

---

## customers

| Issue | Where | Intended For |
|-------|-------|--------------|
| Duplicate customers (same email, different ID) | 15 rows | Deduplication strategies, entity resolution |
| Missing emails | 20 rows | Missing value detection and handling |
| Invalid email formats | 10 rows | Email validation patterns, regex filtering |
| Missing phone numbers | 15 rows | Nullable field handling |
| Phone number format inconsistency | Mixed formats | String parsing, normalization |
| Future signup dates | 5 rows | Temporal validation, date range filtering |
| State format inconsistency | 8 rows (full name vs code) | Categorical value standardization |

## products

| Issue | Where | Intended For |
|-------|-------|--------------|
| Missing price values | 3 rows | Null/NaN handling in numeric columns |
| Category casing inconsistency | 8 rows (lowercase, UPPERCASE, underscore) | Categorical normalization, groupby alignment |

## orders

| Issue | Where | Intended For |
|-------|-------|--------------|
| Future order dates | 10 rows | Temporal data validation |
| Invalid/mixed-case status values | 8 rows (pending, delivered, returned, unknown, COMPLETED, Shipped) | Status normalization, categorical cleaning |
| Negative totals | 5 rows | Numeric validation, sign checking |
| Orphaned customer references | 12 rows (non-existent customer_id) | Referential integrity, anti-joins |

## order_items

| Issue | Where | Intended For |
|-------|-------|--------------|
| Negative quantities | 20 rows | Business logic validation |
| Zero quantities | 15 rows | Edge case filtering |
| Mismatched line_total | 10 rows | Cross-column consistency checks |
| Orphaned product references | 8 rows (non-existent product_id) | Referential integrity checks |

## payments

| Issue | Where | Intended For |
|-------|-------|--------------|
| Duplicate payment records | 30 rows (same order, different payment_id) | Deduplication, grouping strategies |
| Failed payments on completed orders | 10 rows | Cross-table consistency, status reconciliation |
| Amount mismatch with order total | 5 rows | Cross-table validation, reconciliation |

## shipments

| Issue | Where | Intended For |
|-------|-------|--------------|
| Missing tracking numbers | 25 rows | Missing value patterns in identifiers |
| Missing delivery dates for delivered shipments | 15 rows | Conditional missing value detection |
| Delivery before ship date | 10 rows | Temporal consistency validation |

## reviews

| Issue | Where | Intended For |
|-------|-------|--------------|
| Ratings exceeding valid range (>5) | 10 rows | Range validation, clamping strategies |
| Zero ratings | 5 rows | Boundary value handling |
| Orphaned product references | 15 rows | Referential integrity |
| Empty / whitespace-only review text | 8 rows | String emptiness detection |

## marketing_campaigns

| Issue | Where | Intended For |
|-------|-------|--------------|
| Zero-spend rows | 5 rows | Zero-value filtering, division-by-zero awareness |
| Overlapping date ranges (same channel) | 3 rows (facebook) | Date range overlap detection |
| End date before start date | 4 rows | Temporal range validation |

## website_traffic

| Issue | Where | Intended For |
|-------|-------|--------------|
| Missing dates (gaps) | 10 days skipped | Time series gap detection, resampling |
| Traffic spike anomalies | ~5% of rows | Outlier detection, statistical filtering |
| Multi-dimensional key | Composite (date, device, source) | Multi-index operations, pivot strategies |

## returns

| Issue | Where | Intended For |
|-------|-------|--------------|
| Missing return reasons | 10 rows | Categorical missing value handling |
| Refund amount exceeds original price | 8 rows | Cross-table validation, ratio checks |
| Orphaned order references | 12 rows | Referential integrity |
| Return date before order date | 5 rows | Temporal consistency across tables |
| Negative refund amounts | 7 rows | Numeric sign validation |

---

## Cross-Table Integrity Issues

These issues require joining or comparing multiple tables to detect:

| Issue | Tables Involved | Intended For |
|-------|-----------------|--------------|
| Orders referencing non-existent customers | orders ↔ customers | Anti-joins, set operations |
| Order items referencing non-existent products | order_items ↔ products | Referential integrity |
| Payments with failed status on completed orders | payments ↔ orders | Status reconciliation |
| Payment amounts not matching order totals | payments ↔ orders | Cross-table arithmetic validation |
| Returns referencing non-existent orders | returns ↔ orders | Orphan record detection |
| Return dates preceding order dates | returns ↔ orders | Temporal cross-table validation |
| Refund amounts exceeding original item prices | returns ↔ order_items ↔ products | Multi-table arithmetic validation |
| Shipment statuses inconsistent with order statuses | shipments ↔ orders | Business rule validation |

---

## Format-Specific Challenges

| Issue | File | Intended For |
|-------|------|--------------|
| CSV vs JSON schema mismatch | customers.csv vs customers.json | Format comparison, schema validation |
| CSV vs Parquet column types | orders.csv vs orders.parquet | Type inference differences |
| JSON nested structure | reviews.json, payments.json | JSON parsing, normalization |
| Inconsistent date formats across tables | Multiple | Date parsing strategies |
| Numeric values stored as strings | Multiple CSVs | Type coercion, dtype specification |
