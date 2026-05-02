# Data Dictionary — TechRetail Inc.

## Entity Relationship

```
customers ───┬── orders ─── order_items ─── products
             │                              │
             ├── payments                   ├── reviews
             │                              │
             ├── shipments                  ├── returns
             │
             └── marketing_campaigns (attribution)

website_traffic (standalone, daily aggregates)
```

---

## 1. customers

**Format:** CSV + JSON
**Records:** ~515 (includes intentional duplicates)
**File:** `customers.csv`, `customers.json`

| Column | Type | Description |
|--------|------|-------------|
| customer_id | string | Unique identifier, format `C00001` |
| first_name | string | Customer first name |
| last_name | string | Customer last name |
| email | string | Email address (may be empty/invalid) |
| phone | string | Phone number in various formats |
| city | string | City name |
| state | string | State code or full name |
| zip_code | string | 5-digit ZIP |
| signup_date | date | Account creation date (YYYY-MM-DD) |
| membership | string | basic / silver / gold / platinum |
| source | string | Acquisition channel |

**Key:** `customer_id`

---

## 2. products

**Format:** CSV
**Records:** 150 (12 products × 6 categories)
**File:** `products.csv`

| Column | Type | Description |
|--------|------|-------------|
| product_id | string | Unique identifier, format `P0001` |
| product_name | string | Product name |
| category | string | Category (inconsistent casing) |
| price | float | Retail price (may be empty) |
| cost | float | Wholesale cost |
| supplier | string | Supplier name |
| rating | float | Average rating (1.0–5.0) |
| stock_quantity | int | Current inventory |
| weight_kg | float | Product weight |
| sku | string | Stock keeping unit |
| launch_date | date | Product launch date |

**Key:** `product_id`

---

## 3. orders

**Format:** CSV + Parquet
**Records:** 5,000
**File:** `orders.csv`, `orders.parquet`

| Column | Type | Description |
|--------|------|-------------|
| order_id | string | Unique identifier, format `ORD-000001` |
| customer_id | string | FK → customers.customer_id |
| order_date | date | Order date (YYYY-MM-DD) |
| status | string | completed / shipped / processing / cancelled / refunded |
| subtotal | float | Line items total |
| discount_pct | float | Discount percentage |
| shipping_cost | float | Shipping fee |
| tax | float | Tax amount |
| total | float | Final total (may be negative) |
| payment_method | string | credit_card / paypal / etc. |
| coupon_code | string | Applied coupon or empty |

**Key:** `order_id`

---

## 4. order_items

**Format:** CSV
**Records:** ~12,000
**File:** `order_items.csv`

| Column | Type | Description |
|--------|------|-------------|
| item_id | string | Unique identifier, format `ITEM-000001` |
| order_id | string | FK → orders.order_id |
| product_id | string | FK → products.product_id |
| quantity | int | Units ordered (may be negative/zero) |
| unit_price | float | Price per unit |
| line_total | float | quantity × unit_price (may be inconsistent) |

**Key:** `item_id`

---

## 5. payments

**Format:** CSV + JSON
**Records:** ~5,530 (includes duplicates)
**File:** `payments.csv`, `payments.json`

| Column | Type | Description |
|--------|------|-------------|
| payment_id | string | Unique identifier, format `PAY-000001` |
| order_id | string | FK → orders.order_id |
| method | string | Payment method |
| amount | float | Payment amount |
| status | string | completed / failed / pending / refunded |
| transaction_date | datetime | Transaction timestamp |
| currency | string | USD / EUR / GBP / CAD |
| auth_code | string | Authorization code |

**Key:** `payment_id`

---

## 6. shipments

**Format:** CSV
**Records:** ~4,500
**File:** `shipments.csv`

| Column | Type | Description |
|--------|------|-------------|
| shipment_id | string | Unique identifier, format `SHP-000001` |
| order_id | string | FK → orders.order_id |
| carrier | string | USPS / UPS / FedEx / DHL / Amazon Logistics |
| tracking_number | string | Tracking code (may be empty) |
| ship_date | date | Shipment date |
| delivery_date | date | Delivery date (may be empty) |
| status | string | delivered / in_transit / out_for_delivery / returned |
| shipping_address | string | Street address |
| city | string | City |
| state | string | State |
| zip | string | ZIP code |

**Key:** `shipment_id`

---

## 7. reviews

**Format:** JSON
**Records:** 2,000
**File:** `reviews.json`

| Column | Type | Description |
|--------|------|-------------|
| review_id | string | Unique identifier, format `REV-00001` |
| product_id | string | FK → products.product_id |
| customer_id | string | FK → customers.customer_id |
| rating | int | 1–5 (may exceed range) |
| review_text | string | Review content (may be empty) |
| review_date | date | Review date |
| verified_purchase | bool | Whether buyer verified |
| helpful_votes | int | Number of helpful votes |

**Key:** `review_id`

---

## 8. marketing_campaigns

**Format:** CSV
**Records:** 50
**File:** `marketing_campaigns.csv`

| Column | Type | Description |
|--------|------|-------------|
| campaign_id | string | Unique identifier, format `CMP-0001` |
| channel | string | google_ads / facebook / instagram / etc. |
| campaign_name | string | Campaign name |
| start_date | date | Campaign start |
| end_date | date | Campaign end |
| budget | float | Planned budget |
| actual_spend | float | Actual spend (may be zero) |
| impressions | int | Ad impressions |
| clicks | int | Ad clicks |
| conversions | int | Conversions |
| ctr | float | Click-through rate (%) |
| cpa | float | Cost per acquisition |

**Key:** `campaign_id`

---

## 9. website_traffic

**Format:** CSV
**Records:** ~355 (daily, with gaps)
**File:** `website_traffic.csv`

| Column | Type | Description |
|--------|------|-------------|
| date | date | Date (YYYY-MM-DD) |
| sessions | int | Number of sessions |
| bounces | int | Bounced sessions |
| conversions | int | Conversions |
| pageviews | int | Total page views |
| avg_session_duration_sec | float | Average session duration |
| bounce_rate | float | Bounce rate (%) |
| conversion_rate | float | Conversion rate (%) |
| new_users | int | New user count |
| returning_users | int | Returning user count |
| device | string | desktop / mobile / tablet |
| traffic_source | string | organic / direct / referral / etc. |

**Key:** composite (`date`, `device`, `traffic_source`)

---

## 10. returns

**Format:** CSV
**Records:** 350
**File:** `returns.csv`

| Column | Type | Description |
|--------|------|-------------|
| return_id | string | Unique identifier, format `RET-00001` |
| order_id | string | FK → orders.order_id |
| product_id | string | FK → products.product_id |
| reason | string | Return reason (may be empty) |
| return_date | date | Return request date |
| refund_amount | float | Refund amount (may be negative or inflated) |
| refund_method | string | original_payment / store_credit / exchange |
| processing_days | int | Days to process |
| condition | string | unopened / opened / used / damaged |
| customer_satisfaction | int | 1–5 satisfaction rating |

**Key:** `return_id`
