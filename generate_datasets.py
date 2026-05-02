#!/usr/bin/env python3
"""
Generate three interconnected datasets for pandas practice:
1. clients.csv - Client identification data (B2B & B2C)
2. promotions.tsv - Marketing promotions table
3. transactions.json - Customer transactions with campaign attribution
"""

import csv
import json
import os
import random
import uuid
from datetime import datetime, timedelta

random.seed(42)

# ============================================================
# Configuration
# ============================================================
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")
NUM_CLIENTS = 50000
NUM_PROMOTIONS = 80
NUM_TRANSACTIONS = 200000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Reference Data
# ============================================================
COUNTRIES = [
    ("US", "United States"), ("GB", "United Kingdom"), ("DE", "Germany"),
    ("FR", "France"), ("JP", "Japan"), ("CA", "Canada"), ("AU", "Australia"),
    ("BR", "Brazil"), ("IN", "India"), ("MX", "Mexico"), ("IT", "Italy"),
    ("ES", "Spain"), ("NL", "Netherlands"), ("SE", "Sweden"), ("CH", "Switzerland"),
    ("SG", "Singapore"), ("KR", "South Korea"), ("CN", "China"),
    ("ZA", "South Africa"), ("AE", "United Arab Emirates"),
]

COMPANY_SUFFIXES = [
    "Inc", "LLC", "Corp", "Ltd", "GmbH", "SA", "SARL", "Pty Ltd",
    "K.K.", "S.A.", "AG", "BV", "AB", "Pte Ltd", "LLP",
]

FIRST_NAMES_M = [
    "James", "John", "Robert", "Michael", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony",
    "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth",
    "Liam", "Noah", "Oliver", "Elijah", "Lucas", "Mason", "Logan",
    "Hugo", "Luca", "Marco", "Klaus", "Hans", "Pierre", "Jean",
    "Takeshi", "Hiroshi", "Yuki", "Raj", "Arjun", "Carlos", "Miguel",
]

FIRST_NAMES_F = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret",
    "Sandra", "Ashley", "Dorothy", "Kimberly", "Emily", "Donna",
    "Olivia", "Emma", "Ava", "Sophia", "Isabella", "Mia", "Charlotte",
    "Ingrid", "Greta", "Marie", "Françoise", "Yoko", "Priya", "Ana",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Park", "Kim", "Patel", "Singh", "Kumar", "Müller", "Schmidt",
    "Schneider", "Fischer", "Weber", "Dubois", "Martin", "Bernard",
    "Yamamoto", "Nakamura", "Tanaka", "Silva", "Santos", "Costa",
    "Ferreira", "Rossi", "Ferrari", "Bianchi", "Romano", "Colombo",
]

COMPANY_PREFIXES = [
    "Apex", "Global", "Prime", "Summit", "Nexus", "Vertex", "Zenith",
    "Quantum", "Horizon", "Pinnacle", "Atlas", "Titan", "Omega",
    "Stellar", "Phoenix", "Vanguard", "Meridian", "Cascade", "Fusion",
    "Innovate", "Synergy", "Momentum", "Catalyst", "Elevate", "Crest",
    "Bridge", "Core", "Edge", "Forge", "Grid", "Hub", "Link",
    "Nova", "Orbit", "Peak", "Ridge", "Scope", "Shift", "Spark",
    "Tech", "Unity", "Vector", "Wave", "Axis", "Bolt", "Cloud",
    "Data", "Echo", "Flow", "Growth", "Harbor", "Insight", "Junction",
]

INDUSTRIES = [
    "Technology", "Finance", "Healthcare", "Manufacturing", "Retail",
    "Education", "Energy", "Telecommunications", "Transportation",
    "Real Estate", "Consulting", "Media", "Agriculture", "Construction",
    "Insurance", "Pharmaceuticals", "Automotive", "Food & Beverage",
    "Hospitality", "Logistics",
]

CURRENCIES_BY_COUNTRY = {
    "US": "USD", "GB": "GBP", "DE": "EUR", "FR": "EUR", "JP": "JPY",
    "CA": "CAD", "AU": "AUD", "BR": "BRL", "IN": "INR", "MX": "MXN",
    "IT": "EUR", "ES": "EUR", "NL": "EUR", "SE": "SEK", "CH": "CHF",
    "SG": "SGD", "KR": "KRW", "CN": "CNY", "ZA": "ZAR", "AE": "AED",
}

PAYMENT_METHODS = ["credit_card", "debit_card", "bank_transfer", "paypal", "invoice", "crypto", "cash"]
TRANSACTION_TYPES = ["purchase", "refund", "subscription", "one_time", "renewal", "upgrade", "downgrade"]
PRODUCT_CATEGORIES = [
    "Software License", "Cloud Services", "Hardware", "Support Contract",
    "Training", "Consulting", "API Access", "Data Storage", "Analytics",
    "Security", "Networking", "Database", "DevOps Tools", "AI/ML Services",
]

PROMOTION_TYPES = ["percentage_discount", "fixed_amount", "free_trial", "bundle_deal", "cashback", "free_shipping"]
CAMPAIGN_CHANNELS = ["email", "social_media", "search_ads", "affiliate", "direct_mail", "webinar", "partner_referral"]

# ============================================================
# Helper Functions
# ============================================================
def random_date(start, end):
    delta = end - start
    if delta.days < 0:
        return start
    random_days = random.randint(0, max(0, delta.days))
    random_seconds = random.randint(0, 86399)
    return start + timedelta(days=random_days, seconds=random_seconds)


def generate_company_name():
    prefix = random.choice(COMPANY_PREFIXES)
    suffix = random.choice(COMPANY_SUFFIXES)
    mid_words = random.sample(["Tech", "Solutions", "Systems", "Digital", "Smart",
                                "Advanced", "Pro", "Elite", "Plus", "Net", "Cloud",
                                "Data", "Soft", "AI", "Labs", "Works"], k=random.randint(0, 2))
    parts = [prefix] + mid_words + [suffix]
    return " ".join(parts)


def generate_email(first_name, last_name, company_name=None):
    domains = ["gmail.com", "outlook.com", "yahoo.com", "protonmail.com"]
    if company_name:
        clean_company = company_name.lower().replace(" ", "").replace(".", "").replace(",", "")
        domains.append(f"{clean_company}.com")
    domain = random.choice(domains)
    patterns = [
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name.lower()[0]}{last_name.lower()}",
        f"{first_name.lower()}_{last_name.lower()}",
        f"{last_name.lower()}.{first_name.lower()}",
    ]
    email = random.choice(patterns)
    if random.random() < 0.1:
        email += str(random.randint(1, 99))
    return f"{email}@{domain}"


def format_currency(amount, currency="USD"):
    return f"{amount:.2f}"


# ============================================================
# Generate Clients Dataset (CSV)
# ============================================================
def generate_clients():
    print("Generating clients...")
    clients = []
    for i in range(NUM_CLIENTS):
        client_id = str(uuid.uuid4())
        country_code, country_name = random.choice(COUNTRIES)

        is_enterprise = random.random() < 0.35
        client_type = random.choice(["enterprise", "enterprise", "smb", "smb", "individual"]) if random.random() < 0.7 else "individual"

        first_name = random.choice(FIRST_NAMES_M + FIRST_NAMES_F)
        last_name = random.choice(LAST_NAMES)

        if client_type in ["enterprise", "smb"]:
            company_name = generate_company_name()
            legal_buyer = f"{random.choice(FIRST_NAMES_M + FIRST_NAMES_F)} {random.choice(LAST_NAMES)}"
            buyer_title = random.choice([
                "Procurement Manager", "VP Purchasing", "CFO", "Director of Operations",
                "Head of Procurement", "Supply Chain Manager", "Chief Operating Officer",
                "Purchasing Director", "Commercial Manager", "Buyer Lead",
            ])
            industry = random.choice(INDUSTRIES)
            employee_count = random.choice([
                random.randint(50, 250),
                random.randint(250, 1000),
                random.randint(1000, 5000),
                random.randint(5000, 20000),
                random.randint(20000, 100000),
            ])
        else:
            company_name = ""
            legal_buyer = ""
            buyer_title = ""
            industry = ""
            employee_count = 0

        email = generate_email(first_name, last_name, company_name if client_type != "individual" else None)
        registration_date = random_date(START_DATE, END_DATE)
        account_status = random.choices(
            ["active", "inactive", "suspended", "pending_verification"],
            weights=[75, 15, 5, 5]
        )[0]

        credit_limit = random.choice([
            0,
            random.randint(1000, 10000),
            random.randint(10000, 50000),
            random.randint(50000, 250000),
            random.randint(250000, 1000000),
        ]) if client_type != "individual" else 0

        loyalty_tier = random.choices(
            ["bronze", "silver", "gold", "platinum", "diamond"],
            weights=[30, 30, 25, 10, 5]
        )[0]

        preferred_language = random.choice(["en", "en", "en", "es", "fr", "de", "ja", "zh", "pt", "hi"])
        marketing_opt_in = random.choice([True, False])
        last_login_date = random_date(registration_date, END_DATE) if account_status == "active" else ""
        lifetime_value = round(random.uniform(100, 500000) if client_type != "individual" else random.uniform(10, 50000), 2)

        tax_id = f"TAX-{random.randint(100000, 999999)}-{random.randint(1000, 9999)}" if client_type != "individual" else ""

        clients.append({
            "client_id": client_id,
            "client_type": client_type,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "company_name": company_name,
            "legal_buyer_name": legal_buyer,
            "legal_buyer_title": buyer_title,
            "industry": industry,
            "employee_count": employee_count,
            "country_code": country_code,
            "country_name": country_name,
            "currency": CURRENCIES_BY_COUNTRY[country_code],
            "account_status": account_status,
            "credit_limit": credit_limit,
            "loyalty_tier": loyalty_tier,
            "preferred_language": preferred_language,
            "marketing_opt_in": marketing_opt_in,
            "registration_date": registration_date.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login_date": last_login_date.strftime("%Y-%m-%d %H:%M:%S") if last_login_date else "",
            "lifetime_value": lifetime_value,
            "tax_id": tax_id,
        })

    filepath = os.path.join(OUTPUT_DIR, "clients.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=clients[0].keys())
        writer.writeheader()
        writer.writerows(clients)

    print(f"  → Wrote {len(clients)} clients to {filepath}")
    return clients


# ============================================================
# Generate Promotions Dataset (TSV)
# ============================================================
def generate_promotions():
    print("Generating promotions...")
    promotions = []
    campaign_count = 25
    campaign_ids = [str(uuid.uuid4()) for _ in range(campaign_count)]

    for i in range(NUM_PROMOTIONS):
        promo_id = str(uuid.uuid4())
        campaign_id = random.choice(campaign_ids)

        promo_code = f"{random.choice(['SAVE', 'DEAL', 'PROMO', 'OFFER', 'DISCOUNT', 'FLASH', 'MEGA', 'SUPER', 'VIP', 'EXCLUSIVE'])}" \
                     f"{random.randint(10, 99)}" \
                     f"{random.choice(['A', 'B', 'C', 'D', 'E', 'X', 'Z'])}"

        promo_type = random.choice(PROMOTION_TYPES)

        if promo_type == "percentage_discount":
            discount_value = random.choice([5, 10, 15, 20, 25, 30, 40, 50])
            discount_unit = "percent"
        elif promo_type == "fixed_amount":
            discount_value = random.choice([10, 25, 50, 100, 250, 500])
            discount_unit = "currency"
        elif promo_type == "cashback":
            discount_value = random.choice([5, 10, 15, 20])
            discount_unit = "percent"
        else:
            discount_value = 0
            discount_unit = "N/A"

        start_date = random_date(START_DATE, END_DATE - timedelta(days=30))
        end_date = start_date + timedelta(days=random.randint(7, 90))

        min_purchase = random.choice([0, 50, 100, 250, 500, 1000])
        max_uses = random.choice([50, 100, 250, 500, 1000, 5000, -1])  # -1 = unlimited
        actual_uses = random.randint(0, max_uses) if max_uses > 0 else random.randint(0, 5000)

        channel = random.choice(CAMPAIGN_CHANNELS)
        is_active = end_date >= datetime.now() and start_date <= datetime.now()

        target_segment = random.choice([
            "all", "new_customers", "enterprise_only", "smb_only", "individual_only",
            "gold_plus", "inactive_reactivation", "high_value", "geo_specific",
        ])

        target_countries = ""
        if target_segment == "geo_specific":
            target_countries = "|".join(random.sample([c[0] for c in COUNTRIES], k=random.randint(1, 5)))

        budget_allocated = round(random.uniform(1000, 100000), 2)
        roi = round(random.uniform(0.5, 5.0), 2) if actual_uses > 0 else 0

        promotions.append({
            "promotion_id": promo_id,
            "promotion_code": promo_code,
            "campaign_id": campaign_id,
            "promotion_type": promo_type,
            "discount_value": discount_value,
            "discount_unit": discount_unit,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "channel": channel,
            "is_active": is_active,
            "target_segment": target_segment,
            "target_countries": target_countries,
            "min_purchase_amount": min_purchase,
            "max_uses": max_uses,
            "actual_uses": actual_uses,
            "budget_allocated": budget_allocated,
            "estimated_roi": roi,
            "created_by": f"marketing_user_{random.randint(1, 20)}",
            "approval_status": random.choices(["approved", "pending", "rejected", "draft"], weights=[70, 15, 5, 10])[0],
        })

    filepath = os.path.join(OUTPUT_DIR, "promotions.tsv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=promotions[0].keys(), delimiter="\t")
        writer.writeheader()
        writer.writerows(promotions)

    print(f"  → Wrote {len(promotions)} promotions to {filepath}")
    return promotions, campaign_ids


# ============================================================
# Generate Transactions Dataset (JSON)
# ============================================================
def generate_transactions(clients, promotions, campaign_ids):
    print("Generating transactions...")

    # Build lookup structures
    client_ids = [c["client_id"] for c in clients]
    client_lookup = {c["client_id"]: c for c in clients}

    promo_lookup = {}
    for p in promotions:
        if p["campaign_id"] not in promo_lookup:
            promo_lookup[p["campaign_id"]] = []
        promo_lookup[p["campaign_id"]].append(p)

    transactions = []

    for i in range(NUM_TRANSACTIONS):
        client = random.choice(clients)
        transaction_date = random_date(START_DATE, END_DATE)

        product_category = random.choice(PRODUCT_CATEGORIES)
        base_amount = random.choice([
            random.uniform(10, 100),
            random.uniform(100, 500),
            random.uniform(500, 2000),
            random.uniform(2000, 10000),
            random.uniform(10000, 50000),
        ])

        currency = client["currency"]

        # ~30% of transactions are tied to marketing campaigns
        has_campaign = random.random() < 0.30
        campaign_id = ""
        promotion_code = ""
        discount_applied = 0
        final_amount = base_amount

        if has_campaign:
            campaign_id = random.choice(campaign_ids)
            if campaign_id in promo_lookup:
                promo = random.choice(promo_lookup[campaign_id])
                promotion_code = promo["promotion_code"]

                if promo["promotion_type"] == "percentage_discount":
                    discount_applied = round(base_amount * (promo["discount_value"] / 100), 2)
                    final_amount = base_amount - discount_applied
                elif promo["promotion_type"] == "fixed_amount":
                    discount_applied = min(promo["discount_value"], base_amount)
                    final_amount = base_amount - discount_applied
                elif promo["promotion_type"] == "cashback":
                    discount_applied = round(base_amount * (promo["discount_value"] / 100), 2)
                    final_amount = base_amount
                else:
                    final_amount = base_amount
        else:
            final_amount = base_amount

        transaction_type = random.choice(TRANSACTION_TYPES)
        if transaction_type == "refund":
            final_amount = -abs(final_amount)
            discount_applied = -abs(discount_applied)

        payment_method = random.choice(PAYMENT_METHODS)

        # Generate a realistic transaction reference
        txn_ref = f"TXN-{transaction_date.strftime('%Y%m%d')}-{random.randint(100000, 999999)}"

        # Regional tax / VAT
        tax_rate = random.choice([0, 0.05, 0.07, 0.08, 0.10, 0.15, 0.19, 0.20, 0.21, 0.25])
        tax_amount = round(final_amount * tax_rate, 2)

        invoice_number = f"INV-{random.randint(100000, 999999)}-{random.randint(10, 99)}"

        satisfaction_score = random.choices([1, 2, 3, 4, 5], weights=[2, 5, 15, 35, 43])[0]

        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "client_id": client["client_id"],
            "transaction_date": transaction_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "product_category": product_category,
            "base_amount": round(base_amount, 2),
            "discount_applied": round(discount_applied, 2),
            "tax_amount": tax_amount,
            "final_amount": round(final_amount + tax_amount, 2),
            "currency": currency,
            "payment_method": payment_method,
            "transaction_type": transaction_type,
            "campaign_id": campaign_id,
            "promotion_code": promotion_code,
            "invoice_number": invoice_number,
            "transaction_reference": txn_ref,
            "is_campaign_transaction": has_campaign,
            "satisfaction_score": satisfaction_score,
            "processing_time_ms": random.randint(50, 5000),
            "region": client["country_name"],
        }

        transactions.append(transaction)

    filepath = os.path.join(OUTPUT_DIR, "transactions.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2)

    print(f"  → Wrote {len(transactions)} transactions to {filepath}")
    return transactions


# ============================================================
# Main Execution
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Dataset Generation for Pandas Practice")
    print("=" * 60)

    clients = generate_clients()
    promotions, campaign_ids = generate_promotions()
    transactions = generate_transactions(clients, promotions, campaign_ids)

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"  clients.csv        → {len(clients):>8,} rows  (client identification)")
    print(f"  promotions.tsv     → {len(promotions):>8,} rows  (marketing promotions)")
    print(f"  transactions.json  → {len(transactions):>8,} rows  (customer transactions)")
    print("\nJoin Keys:")
    print("  clients.client_id == transactions.client_id  (1-to-many)")
    print("  promotions.campaign_id == transactions.campaign_id  (1-to-many)")
    print("  promotions can be grouped by campaign_id for campaign-level analysis")
    print("\nNotable Stats:")
    print(f"  - {sum(1 for c in clients if c['client_type'] != 'individual'):,} B2B clients (enterprise + SMB)")
    print(f"  - {sum(1 for c in clients if c['client_type'] == 'individual'):,} B2C clients")
    print(f"  - {sum(1 for t in transactions if t['is_campaign_transaction']):,} transactions tied to campaigns ({sum(1 for t in transactions if t['is_campaign_transaction'])/len(transactions)*100:.1f}%)")
    print(f"  - {len(set(t['campaign_id'] for t in transactions if t['campaign_id'])):,} unique campaigns in transactions")
    print(f"  - {len(COUNTRIES)} countries represented")
    print(f"  - Date range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
