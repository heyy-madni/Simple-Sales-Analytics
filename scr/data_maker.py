import sqlite3
import random
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict

random.seed(42)
np.random.seed(42)

# ------------------------
# DATABASE SETUP
# ------------------------

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);
""")

# ------------------------
# DATA CONFIG
# ------------------------

NUM_CUSTOMERS = 1200
MIN_ORDERS = 26000

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

cities = ["Mumbai","Delhi","Bangalore","Surat","Ahmedabad",
          "Pune","Hyderabad","Chennai","Kolkata"]

first_names = ["Aarav","Vivaan","Aditya","Vihaan","Arjun","Sai",
               "Ananya","Diya","Myra","Sara","Priya","Isha"]

last_names = ["Sharma","Patel","Verma","Gupta","Mehta",
              "Reddy","Nair","Rao","Khan","Joshi"]

# ------------------------
# INSERT CUSTOMERS
# ------------------------

customers = []
segments = {}

high = int(NUM_CUSTOMERS * 0.10)
medium = int(NUM_CUSTOMERS * 0.30)
low = NUM_CUSTOMERS - high - medium

cid = 1

def random_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

for _ in range(high):
    customers.append((cid, random_name(), random.choice(cities)))
    segments[cid] = "high"
    cid += 1

for _ in range(medium):
    customers.append((cid, random_name(), random.choice(cities)))
    segments[cid] = "medium"
    cid += 1

for _ in range(low):
    customers.append((cid, random_name(), random.choice(cities)))
    segments[cid] = "low"
    cid += 1

cursor.executemany("INSERT INTO customers VALUES (?, ?, ?);", customers)

# ------------------------
# INSERT PRODUCTS
# ------------------------

categories = {
    "Electronics": (8000, 60000),
    "Clothing": (500, 4000),
    "Home": (1000, 15000),
    "Sports": (700, 10000),
    "Accessories": (200, 2000)
}

products = []
product_prices = {}
product_categories = {}

pid = 1

for cat, (low_p, high_p) in categories.items():
    for i in range(10):
        price = round(random.uniform(low_p, high_p), 2)
        products.append((pid, f"{cat} Product {i+1}", cat, price))
        product_prices[pid] = price
        product_categories[pid] = cat
        pid += 1

cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?);", products)

# ------------------------
# ORDER GENERATION
# ------------------------

def random_date():
    delta = END_DATE - START_DATE
    while True:
        d = START_DATE + timedelta(days=random.randint(0, delta.days))
        if d.month == 2 and random.random() < 0.3:
            continue
        return d.strftime("%Y-%m-%d")

def get_purchase_count(segment):
    if segment == "high":
        return random.randint(20, 35)
    elif segment == "medium":
        return random.randint(8, 15)
    return random.randint(1, 5)

orders = []
oid = 1

for cid in segments:
    for _ in range(get_purchase_count(segments[cid])):
        pid = random.choice(products)[0]
        category = product_categories[pid]

        if category == "Electronics":
            qty = 1
        elif category == "Accessories":
            qty = random.randint(2, 4)
        else:
            qty = random.randint(1, 3)

        orders.append((oid, cid, pid, qty, random_date()))
        oid += 1

while len(orders) < MIN_ORDERS:
    cid = random.choice(list(segments.keys()))
    pid = random.choice(products)[0]
    category = product_categories[pid]

    if category == "Electronics":
        qty = 1
    elif category == "Accessories":
        qty = random.randint(2, 4)
    else:
        qty = random.randint(1, 3)

    orders.append((oid, cid, pid, qty, random_date()))
    oid += 1

cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?);", orders)

# ------------------------
# COMMIT & CLOSE
# ------------------------

conn.commit()
conn.close()

print("Database created successfully: database.db")
print("Total Orders Inserted:", len(orders))