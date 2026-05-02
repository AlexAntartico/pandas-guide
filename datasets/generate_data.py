#!/usr/bin/env python3
"""Generate realistic, intentionally messy datasets for pandas practice.
TechRetail Inc. — multi-table e-commerce scenario.
"""

import csv
import json
import os
import random
import string
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

BASE = Path(__file__).parent / "raw"
BASE.mkdir(parents=True, exist_ok=True)

# ─── helpers ───────────────────────────────────────────────────────────────
def rand_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def rand_choice(pop, p=None):
    return random.choices(pop, weights=p, k=1)[0] if p else random.choice(pop)

def fake_email(first, last, domain=None):
    domains = domain or random.choice(["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "proton.me"])
    sep = random.choice([".", "_", "", ""])
    return f"{first.lower()}{sep}{last.lower()}@{domains}"

def fake_phone():
    fmt = random.choice([
        lambda: f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        lambda: f"({random.randint(200,999)}) {random.randint(100,999)}-{random.randint(1000,9999)}",
        lambda: f"{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        lambda: f"{random.randint(200,999)}.{random.randint(100,999)}.{random.randint(1000,9999)}",
        lambda: f"+44 {random.randint(20,99)} {random.randint(1000,9999)} {random.randint(1000,9999)}",
        lambda: "",  # missing
    ])
    return fmt()

FIRST_NAMES = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","David","Elizabeth",
               "William","Barbara","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Charles","Karen",
               "Christopher","Lisa","Daniel","Nancy","Matthew","Betty","Anthony","Margaret","Mark","Sandra",
               "Donald","Ashley","Steven","Dorothy","Paul","Kimberly","Andrew","Emily","Joshua","Donna",
               "Kenneth","Michelle","Kevin","Carol","Brian","Amanda","George","Melissa","Timothy","Deborah",
               "Ronald","Stephanie","Edward","Rebecca","Jason","Sharon","Jeffrey","Laura","Ryan","Cynthia",
               "Jacob","Kathleen","Gary","Amy","Nicholas","Angela","Eric","Shirley","Jonathan","Anna",
               "Stephen","Brenda","Larry","Pamela","Justin","Emma","Scott","Nicole","Brandon","Helen",
               "Benjamin","Samantha","Samuel","Katherine","Raymond","Christine","Gregory","Debra","Frank","Rachel",
               "Alexander","Carolyn","Patrick","Janet","Jack","Catherine","Dennis","Maria","Jerry","Heather",
               "Tyler","Diane","Aaron","Ruth","Jose","Julie","Adam","Olivia","Nathan","Diana"]

LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
              "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
              "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
              "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
              "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts",
              "Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes",
              "Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper",
              "Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson",
              "Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes",
              "Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross","Foster","Jimenez"]

CITIES = ["New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio","San Diego",
          "Dallas","San Jose","Austin","Jacksonville","Fort Worth","Columbus","Charlotte","Indianapolis",
          "San Francisco","Seattle","Denver","Washington","Boston","Nashville","Portland","Oklahoma City",
          "Las Vegas","Louisville","Baltimore","Milwaukee","Albuquerque","Tucson","Fresno","Sacramento",
          "Kansas City","Mesa","Atlanta","Omaha","Colorado Springs","Raleigh","Miami","Long Beach",
          "London","Toronto","Sydney","Berlin","Tokyo","Singapore","Mumbai","São Paulo","Cape Town","Lagos"]

STATES = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME",
          "MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA",
          "RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"]

# ─── 1. CUSTOMERS ─────────────────────────────────────────────────────────
def gen_customers():
    rows = []
    seen_emails = set()
    for i in range(1, 501):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        email = fake_email(first, last)
        while email in seen_emails:
            email = fake_email(first, last, random.choice(["gmail.com","yahoo.com","outlook.com"]))
        seen_emails.add(email)
        phone = fake_phone()
        city = random.choice(CITIES)
        state = random.choice(STATES) if city in STATES or len(city) < 12 else random.choice(STATES)
        signup = rand_date(datetime(2020, 1, 1), datetime(2025, 4, 30))
        rows.append({
            "customer_id": f"C{i:05d}",
            "first_name": first,
            "last_name": last,
            "email": email,
            "phone": phone,
            "city": city,
            "state": state,
            "zip_code": f"{random.randint(10001, 99950)}",
            "signup_date": signup.strftime("%Y-%m-%d"),
            "membership": rand_choice(["basic","basic","basic","silver","gold","platinum"],
                                      p=[40,15,15,12,10,8]),
            "source": rand_choice(["organic","google","facebook","instagram","referral","email","tiktok"],
                                  p=[25,20,15,10,12,10,8]),
        })

    # Dirty: inject 15 duplicate customers (same email, different ID)
    dupes = random.sample(rows, 15)
    for d in dupes:
        dup = d.copy()
        dup["customer_id"] = f"C{random.randint(501,600):05d}"
        dup["email"] = d["email"]  # same email
        dup["signup_date"] = (datetime.strptime(d["signup_date"], "%Y-%m-%d") + timedelta(days=random.randint(1,90))).strftime("%Y-%m-%d")
        rows.append(dup)

    # Dirty: 20 missing emails
    for r in random.sample(rows, 20):
        r["email"] = ""

    # Dirty: 10 invalid emails
    for r in random.sample(rows, 10):
        r["email"] = random.choice(["not-an-email", "missing@", "@nodomain.com", "space name@test.com", ""])

    # Dirty: 15 missing phones
    for r in random.sample(rows, 15):
        r["phone"] = ""

    # Dirty: 5 future signup dates
    for r in random.sample(rows, 5):
        r["signup_date"] = rand_date(datetime(2026, 1, 1), datetime(2026, 12, 31)).strftime("%Y-%m-%d")

    # Dirty: 8 inconsistent state formats
    state_map = {"CA": "California", "NY": "New York", "TX": "Texas", "FL": "Florida"}
    for r in random.sample(rows, 8):
        if r["state"] in state_map:
            r["state"] = state_map[r["state"]]

    df = pd.DataFrame(rows)
    df.to_csv(BASE / "customers.csv", index=False)

    # Also export as JSON
    with open(BASE / "customers.json", "w") as f:
        json.dump(rows, f, indent=2)

    return rows

# ─── 2. PRODUCTS ──────────────────────────────────────────────────────────
def gen_products():
    categories = {
        "Electronics": ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch", "Speaker", "Monitor", "Keyboard", "Mouse", "Webcam", "Charger", "Cable"],
        "Clothing": ["T-Shirt", "Jeans", "Jacket", "Dress", "Sweater", "Hoodie", "Shorts", "Skirt", "Coat", "Socks", "Hat", "Scarf"],
        "Home & Kitchen": ["Blender", "Toaster", "Coffee Maker", "Vacuum", "Lamp", "Pillow", "Towel Set", "Cutting Board", "Knife Set", "Rice Cooker", "Mug", "Plate Set"],
        "Books": ["Novel", "Textbook", "Cookbook", "Biography", "Sci-Fi", "Self-Help", "History", "Art Book", "Travel Guide", "Comic", "Dictionary", "Journal"],
        "Sports": ["Yoga Mat", "Dumbbells", "Running Shoes", "Basketball", "Tennis Racket", "Bicycle Helmet", "Water Bottle", "Jump Rope", "Resistance Bands", "Gym Bag", "Fitness Tracker", "Foam Roller"],
        "Beauty": ["Moisturizer", "Shampoo", "Sunscreen", "Lip Balm", "Face Mask", "Perfume", "Nail Polish", "Hair Dryer", "Makeup Kit", "Body Lotion", "Eye Cream", "Serum"],
    }
    rows = []
    pid = 1
    for cat, items in categories.items():
        for item in items:
            base_price = random.choice([9.99, 14.99, 19.99, 24.99, 29.99, 39.99, 49.99, 59.99, 79.99, 99.99, 149.99, 199.99, 299.99, 499.99, 799.99, 999.99])
            cost = round(base_price * random.uniform(0.25, 0.65), 2)
            supplier = random.choice(["TechSupply Co", "GlobalGoods", "DirectMfg", "WholesalePlus", "PrimeSource"])
            rating = round(random.uniform(1.0, 5.0), 1)
            stock = random.randint(0, 500)

            # Dirty: 3 products with null/missing prices
            if pid in [7, 42, 88]:
                price_str = ""
            else:
                price_str = f"{base_price:.2f}"

            # Dirty: inconsistent category naming
            cat_display = cat
            if pid in [13, 14, 15]:
                cat_display = "electronics"  # lowercase
            elif pid in [25, 26]:
                cat_display = "HOME & KITCHEN"  # uppercase
            elif pid in [37, 38]:
                cat_display = "home_kitchen"  # underscore

            rows.append({
                "product_id": f"P{pid:04d}",
                "product_name": item,
                "category": cat_display,
                "price": price_str,
                "cost": f"{cost:.2f}",
                "supplier": supplier,
                "rating": rating,
                "stock_quantity": stock,
                "weight_kg": round(random.uniform(0.1, 15.0), 2),
                "sku": f"SKU-{random.randint(10000,99999)}",
                "launch_date": rand_date(datetime(2021, 1, 1), datetime(2025, 3, 1)).strftime("%Y-%m-%d"),
            })
            pid += 1

    df = pd.DataFrame(rows)
    df.to_csv(BASE / "products.csv", index=False)
    return rows

# ─── 3. ORDERS ────────────────────────────────────────────────────────────
def gen_orders(customers):
    statuses = ["completed", "completed", "completed", "completed", "shipped", "processing", "cancelled", "refunded"]
    order_ids = []
    rows = []
    for i in range(1, 5001):
        cust = random.choice(customers)
        status = rand_choice(statuses, p=[50,5,10,5,15,8,5,2])
        order_date = rand_date(datetime(2022, 1, 1), datetime(2025, 4, 28))
        total = round(random.uniform(15, 2500), 2)
        discount = round(random.choice([0,0,0,0,0,5,10,15,20,25]), 2)

        rows.append({
            "order_id": f"ORD-{i:06d}",
            "customer_id": cust["customer_id"],
            "order_date": order_date.strftime("%Y-%m-%d"),
            "status": status,
            "subtotal": f"{total:.2f}",
            "discount_pct": f"{discount:.2f}",
            "shipping_cost": f"{round(random.choice([0,0,0,5.99,7.99,9.99,12.99,15.99,24.99]), 2):.2f}",
            "tax": f"{round(total * 0.08, 2):.2f}",
            "total": f"{round(total * (1 - discount/100) + random.choice([0,0,0,5.99,7.99,9.99,12.99,15.99,24.99]) + total * 0.08, 2):.2f}",
            "payment_method": rand_choice(["credit_card","credit_card","credit_card","debit_card","paypal","apple_pay","google_pay","bank_transfer"]),
            "coupon_code": random.choice(["", "", "", "", "", "SAVE10", "WELCOME20", "FLASH15", "VIP25", ""]),
        })
        order_ids.append(f"ORD-{i:06d}")

    # Dirty: 10 orders with future dates
    for r in random.sample(rows, 10):
        r["order_date"] = rand_date(datetime(2026, 1, 1), datetime(2026, 6, 1)).strftime("%Y-%m-%d")

    # Dirty: 8 orders with invalid status
    for r in random.sample(rows, 8):
        r["status"] = random.choice(["pending", "delivered", "returned", "unknown", "COMPLETED", "Shipped"])

    # Dirty: 5 orders with negative total
    for r in random.sample(rows, 5):
        r["total"] = f"-{r['total']}"

    # Dirty: 12 orders referencing non-existent customers
    for r in random.sample(rows, 12):
        r["customer_id"] = f"C{random.randint(700,900):05d}"

    df = pd.DataFrame(rows)
    df.to_csv(BASE / "orders.csv", index=False)
    # Also parquet
    df.to_parquet(BASE / "orders.parquet", index=False)
    return rows, order_ids

# ─── 4. ORDER ITEMS ───────────────────────────────────────────────────────
def gen_order_items(products, orders, order_ids):
    rows = []
    item_id = 1
    for order in orders:
        n_items = random.randint(1, 5)
        prods = random.sample(products, min(n_items, len(products)))
        for p in prods:
            qty = random.randint(1, 4)
            price = float(p["price"]) if p["price"] else round(random.uniform(10, 200), 2)
            rows.append({
                "item_id": f"ITEM-{item_id:06d}",
                "order_id": order["order_id"],
                "product_id": p["product_id"],
                "quantity": qty,
                "unit_price": f"{price:.2f}",
                "line_total": f"{round(price * qty, 2):.2f}",
            })
            item_id += 1

    # Dirty: 20 negative quantities
    for r in random.sample(rows, 20):
        r["quantity"] = -abs(int(r["quantity"]))

    # Dirty: 15 zero quantities
    for r in random.sample(rows, 15):
        r["quantity"] = 0

    # Dirty: 10 mismatched line_total
    for r in random.sample(rows, 10):
        r["line_total"] = f"{round(float(r['unit_price']) * abs(int(r['quantity'])) * random.uniform(0.5, 2.0), 2):.2f}"

    # Dirty: 8 items referencing non-existent products
    for r in random.sample(rows, 8):
        r["product_id"] = f"P{random.randint(200,300):04d}"

    df = pd.DataFrame(rows)
    df.to_csv(BASE / "order_items.csv", index=False)

# ─── 5. PAYMENTS ──────────────────────────────────────────────────────────
def gen_payments(orders):
    methods = ["credit_card", "debit_card", "paypal", "apple_pay", "google_pay", "bank_transfer"]
    rows = []
    pid = 1
    for order in orders:
        total = abs(float(order["total"]))
        method = order["payment_method"]
        status = rand_choice(["completed","completed","completed","completed","completed","failed","pending","refunded"],
                             p=[40,10,10,10,10,8,7,5])
        txn_date = datetime.strptime(order["order_date"], "%Y-%m-%d") + timedelta(hours=random.randint(0, 48))

        rows.append({
            "payment_id": f"PAY-{pid:06d}",
            "order_id": order["order_id"],
            "method": method,
            "amount": f"{total:.2f}",
            "status": status,
            "transaction_date": txn_date.strftime("%Y-%m-%d %H:%M:%S"),
            "currency": random.choice(["USD","USD","USD","USD","USD","EUR","GBP","CAD"]),
            "auth_code": f"AUTH-{random.randint(100000,999999)}",
        })
        pid += 1

    # Dirty: 30 duplicate payments (same order, different payment_id)
    dups = random.sample(rows, 30)
    for d in dups:
        dup = d.copy()
        dup["payment_id"] = f"PAY-{pid:06d}"
        dup["status"] = "completed"
        rows.append(dup)
        pid += 1

    # Dirty: 10 failed payments with completed status in order
    for r in random.sample(rows, 10):
        r["status"] = "failed"

    # Dirty: 5 amounts that don't match order total
    for r in random.sample(rows, 5):
        r["amount"] = f"{round(float(r['amount']) * random.uniform(0.5, 1.5), 2):.2f}"

    df = pd.DataFrame(rows)
    df.to_csv(BASE / "payments.csv", index=False)

    # JSON export
    with open(BASE / "payments.json", "w") as f:
        json.dump([dict(r) for r in rows], f, indent=2)

# ─── 6. SHIPMENTS ─────────────────────────────────────────────────────────
def gen_shipments(orders):
    carriers = ["USPS", "UPS", "FedEx", "DHL", "Amazon Logistics"]
    rows = []
    sid = 1
    for order in orders:
        if order["status"] in ["cancelled", "refunded"]:
            continue
        order_dt = datetime.strptime(order["order_date"], "%Y-%m-%d")
        ship_date = order_dt + timedelta(days=random.randint(1, 5))
        deliver_date = ship_date + timedelta(days=random.randint(1, 14))

        rows.append({
            "shipment_id": f"SHP-{sid:06d}",
            "order_id": order["order_id"],
            "carrier": random.choice(carriers),
            "tracking_number": f"{random.choice(['1Z','9400','792','LD'])}{random.randint(100000000,999999999)}" if random.random() > 0.1 else "",
            "ship_date": ship_date.strftime("%Y-%m-%d"),
            "delivery_date": deliver_date.strftime("%Y-%m-%d") if random.random() > 0.15 else "",
            "status": rand_choice(["delivered","delivered","delivered","in_transit","out_for_delivery","returned"]),
            "shipping_address": f"{random.randint(100,9999)} {random.choice(['Main','Oak','Elm','Pine','Cedar','Maple'])} {random.choice(['St','Ave','Blvd','Dr','Ln'])}",
            "city": random.choice(CITIES[:20]),
            "state": random.choice(STATES[:30]),
            "zip": f"{random.randint(10001,99950)}",
        })
        sid += 1

    # Dirty: 25 missing tracking numbers
    for r in random.sample(rows, min(25, len(rows))):
        r["tracking_number"] = ""

    # Dirty: 15 missing delivery dates for "delivered" shipments
    delivered = [r for r in rows if r["status"] == "delivered"]
    for r in random.sample(delivered, min(15, len(delivered))):
        r["delivery_date"] = ""

    # Dirty: 10 delivery before ship dates
    for r in random.sample(rows, 10):
        r["delivery_date"] = (datetime.strptime(r["ship_date"], "%Y-%m-%d") - timedelta(days=random.randint(1,5))).strftime("%Y-%m-%d")

    df = pd.DataFrame(rows)
    df.to_csv(BASE / "shipments.csv", index=False)

# ─── 7. REVIEWS ───────────────────────────────────────────────────────────
def gen_reviews(products, customers):
    review_texts = [
        "Great product, works exactly as described!",
        "Not bad, but expected better quality for the price.",
        "Absolutely love it! Would buy again.",
        "Arrived damaged, customer service was helpful.",
        "Decent product, nothing special.",
        "Terrible experience. Broke after one week.",
        "Perfect gift! My friend loved it.",
        "Overpriced for what you get.",
        "Exceeded my expectations. Highly recommend.",
        "Meh. It's okay I guess.",
        "Best purchase I've made this year!",
        "Shipping was fast but product was disappointing.",
        "Good value for money.",
        "Could be better. There are cheaper alternatives.",
        "Five stars! No complaints.",
        "",  # empty review
        " ",  # whitespace only
        "N/A",
        "This is an incredibly amazing wonderful fantastic superb outstanding brilliant excellent top-notch phenomenal stellar product that I would highly recommend to everyone I know and love!",  # too long / spam-like
        "bought this 6 months ago and it's still working great",
    ]
    rows = []
    for i in range(1, 2001):
        prod = random.choice(products)
        cust = random.choice(customers)
        rating = rand_choice([1,2,3,4,5], p=[5,10,15,35,35])
        text = random.choice(review_texts)
        review_date = rand_date(datetime(2022, 1, 1), datetime(2025, 4, 28))

        rows.append({
            "review_id": f"REV-{i:05d}",
            "product_id": prod["product_id"],
            "customer_id": cust["customer_id"],
            "rating": rating,
            "review_text": text,
            "review_date": review_date.strftime("%Y-%m-%d"),
            "verified_purchase": random.choice([True, True, True, False]),
            "helpful_votes": random.randint(0, 50),
        })

    # Dirty: 10 ratings > 5
    for r in random.sample(rows, 10):
        r["rating"] = random.choice([6, 7, 8, 10])

    # Dirty: 5 ratings = 0
    for r in random.sample(rows, 5):
        r["rating"] = 0

    # Dirty: 15 referencing non-existent products
    for r in random.sample(rows, 15):
        r["product_id"] = f"P{random.randint(200,300):04d}"

    # Dirty: 8 empty/whitespace review_text
    for r in random.sample(rows, 8):
        r["review_text"] = random.choice(["", " ", "  ", "\t"])

    with open(BASE / "reviews.json", "w") as f:
        json.dump(rows, f, indent=2)

# ─── 8. MARKETING CAMPAIGNS ───────────────────────────────────────────────
def gen_campaigns():
    channels = ["google_ads", "facebook", "instagram", "email", "tiktok", "youtube", "twitter", "linkedin"]
    rows = []
    for i in range(1, 51):
        start = rand_date(datetime(2023, 1, 1), datetime(2025, 4, 1))
        duration = random.randint(7, 90)
        end = start + timedelta(days=duration)
        spend = round(random.uniform(500, 50000), 2)
        impressions = random.randint(10000, 5000000)
        clicks = int(impressions * random.uniform(0.005, 0.08))
        conversions = int(clicks * random.uniform(0.01, 0.15))

        rows.append({
            "campaign_id": f"CMP-{i:04d}",
            "channel": random.choice(channels),
            "campaign_name": f"Q{random.randint(1,4)}_{random.choice(['Brand','Performance','Retargeting','Awareness','Launch'])}_{random.choice(['Spring','Summer','Fall','Winter','Holiday'])}",
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "budget": f"{round(spend * random.uniform(0.8, 1.3), 2):.2f}",
            "actual_spend": f"{spend:.2f}",
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "ctr": f"{round(clicks/impressions*100, 2):.2f}",
            "cpa": f"{round(spend/max(conversions,1), 2):.2f}",
        })

    # Dirty: 5 zero-spend rows
    for r in random.sample(rows, 5):
        r["actual_spend"] = "0.00"
        r["impressions"] = 0
        r["clicks"] = 0

    # Dirty: 3 overlapping date ranges for same channel
    channel_rows = [r for r in rows if r["channel"] == "facebook"]
    if len(channel_rows) >= 3:
        base_date = datetime(2024, 6, 1)
        for r in channel_rows[:3]:
            r["start_date"] = (base_date + timedelta(days=random.randint(0, 10))).strftime("%Y-%m-%d")
            r["end_date"] = (base_date + timedelta(days=random.randint(20, 30))).strftime("%Y-%m-%d")

    # Dirty: 4 end_date before start_date
    for r in random.sample(rows, 4):
        r["end_date"], r["start_date"] = r["start_date"], r["end_date"]

    df = pd.DataFrame(rows)
    df.to_csv(BASE / "marketing_campaigns.csv", index=False)

# ─── 9. WEBSITE TRAFFIC ───────────────────────────────────────────────────
def gen_traffic():
    rows = []
    start = datetime(2024, 1, 1)
    for day in range(365):
        date = start + timedelta(days=day)
        # Skip ~10 random days (gaps)
        if day in random.sample(range(365), 10):
            continue

        base_sessions = random.randint(800, 2500)
        # Weekend dip
        if date.weekday() >= 5:
            base_sessions = int(base_sessions * 0.6)
        # Holiday spike
        if date.month == 12 and date.day >= 20:
            base_sessions = int(base_sessions * 2.5)
        # Random anomaly (5% chance)
        if random.random() < 0.05:
            base_sessions = int(base_sessions * random.uniform(3, 8))

        bounces = int(base_sessions * random.uniform(0.25, 0.55))
        conversions = int(base_sessions * random.uniform(0.01, 0.06))
        pageviews = int(base_sessions * random.uniform(1.5, 4.0))
        avg_duration = round(random.uniform(30, 300), 1)

        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "sessions": base_sessions,
            "bounces": bounces,
            "conversions": conversions,
            "pageviews": pageviews,
            "avg_session_duration_sec": avg_duration,
            "bounce_rate": f"{round(bounces/base_sessions*100, 1):.1f}",
            "conversion_rate": f"{round(conversions/base_sessions*100, 2):.2f}",
            "new_users": int(base_sessions * random.uniform(0.5, 0.8)),
            "returning_users": base_sessions - int(base_sessions * random.uniform(0.5, 0.8)),
            "device": random.choice(["desktop","mobile","tablet"]),
            "traffic_source": rand_choice(["organic","direct","referral","social","paid","email"], p=[30,20,15,15,15,5]),
        })

    df = pd.DataFrame(rows)
    df.to_csv(BASE / "website_traffic.csv", index=False)

# ─── 10. RETURNS ──────────────────────────────────────────────────────────
def gen_returns(orders, products):
    reasons = ["Defective", "Wrong item shipped", "Not as described", "Changed mind", "Size too small",
               "Size too large", "Damaged in shipping", "Late delivery", "Found cheaper elsewhere", "Duplicate order"]
    rows = []
    completed_orders = [o for o in orders if o["status"] in ["completed", "shipped"]]
    for i in range(1, 351):
        order = random.choice(completed_orders)
        prod = random.choice(products)
        order_dt = datetime.strptime(order["order_date"], "%Y-%m-%d")
        return_date = order_dt + timedelta(days=random.randint(3, 60))
        original_price = float(prod["price"]) if prod["price"] else round(random.uniform(10, 200), 2)
        refund = round(original_price * random.uniform(0.5, 1.0), 2)

        rows.append({
            "return_id": f"RET-{i:05d}",
            "order_id": order["order_id"],
            "product_id": prod["product_id"],
            "reason": random.choice(reasons),
            "return_date": return_date.strftime("%Y-%m-%d"),
            "refund_amount": f"{refund:.2f}",
            "refund_method": rand_choice(["original_payment", "store_credit", "exchange"]),
            "processing_days": random.randint(1, 21),
            "condition": rand_choice(["unopened", "opened", "used", "damaged"]),
            "customer_satisfaction": random.randint(1, 5),
        })

    # Dirty: 10 missing reasons
    for r in random.sample(rows, 10):
        r["reason"] = ""

    # Dirty: 8 refund > original price (impossible)
    for r in random.sample(rows, 8):
        r["refund_amount"] = f"{round(float(r['refund_amount']) * random.uniform(1.5, 3.0), 2):.2f}"

    # Dirty: 12 referencing non-existent orders
    for r in random.sample(rows, 12):
        r["order_id"] = f"ORD-{random.randint(6000,8000):06d}"

    # Dirty: 5 return dates before order dates
    for r in random.sample(rows, 5):
        r["return_date"] = (datetime.strptime(r["return_date"], "%Y-%m-%d") - timedelta(days=random.randint(10, 100))).strftime("%Y-%m-%d")

    # Dirty: 7 negative refund amounts
    for r in random.sample(rows, 7):
        r["refund_amount"] = f"-{r['refund_amount']}"

    df = pd.DataFrame(rows)
    df.to_csv(BASE / "returns.csv", index=False)

# ─── MAIN ─────────────────────────────────────────────────────────────────
def main():
    print("Generating datasets...")

    print("  1. Customers (500+ rows)...")
    customers = gen_customers()

    print("  2. Products (150 rows)...")
    products = gen_products()

    print("  3. Orders (5,000 rows)...")
    orders, order_ids = gen_orders(customers)

    print("  4. Order Items (~12,000 rows)...")
    gen_order_items(products, orders, order_ids)

    print("  5. Payments (~5,500 rows)...")
    gen_payments(orders)

    print("  6. Shipments (~4,500 rows)...")
    gen_shipments(orders)

    print("  7. Reviews (2,000 rows)...")
    gen_reviews(products, customers)

    print("  8. Marketing Campaigns (50 rows)...")
    gen_campaigns()

    print("  9. Website Traffic (~355 rows)...")
    gen_traffic()

    print(" 10. Returns (350 rows)...")
    gen_returns(orders, products)

    # List files
    files = sorted(BASE.glob("*"))
    print(f"\nGenerated {len(files)} files in {BASE}/:")
    for f in files:
        size = f.stat().st_size
        if size > 1024:
            print(f"  {f.name:40s} {size/1024:8.1f} KB")
        else:
            print(f"  {f.name:40s} {size:8d} B")

if __name__ == "__main__":
    main()
