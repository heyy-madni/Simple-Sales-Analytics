import sqlite3
import random
from datetime import datetime, timedelta


def make_and_fetch():

    random.seed(42)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        city TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        order_date TEXT
    )
    """)

    NUM_CUSTOMERS = 1200
    MIN_ORDERS = 26000

    START_DATE = datetime(2023, 1, 1)
    END_DATE = datetime(2024, 12, 31)

    cities = ["Mumbai","Delhi","Bangalore","Surat","Ahmedabad","Pune","Hyderabad","Chennai","Kolkata"]

    first_names = ["madni","tofiq","shoaeb","ali","rehan","mahenor","abu","Myra","Sara","aamena","zainab","hussain","sara","mohammed","hassan","faizan","nida","sadia","farhan","aisha"]

    last_names = ["khan","bikari","ansari","shekh","sayyid","maleq","shaikh","mohammed","hussain","siddiqui"]

    customers = []
    segments = {}

    high = int(NUM_CUSTOMERS * 0.1)
    medium = int(NUM_CUSTOMERS * 0.3)
    low = NUM_CUSTOMERS - high - medium

    cid = 1

    for i in range(high):
        name = random.choice(first_names) + " " + random.choice(last_names)
        city = random.choice(cities)
        customers.append((cid, name, city))
        segments[cid] = "high"
        cid += 1

    for i in range(medium):
        name = random.choice(first_names) + " " + random.choice(last_names)
        city = random.choice(cities)
        customers.append((cid, name, city))
        segments[cid] = "medium"
        cid += 1

    for i in range(low):
        name = random.choice(first_names) + " " + random.choice(last_names)
        city = random.choice(cities)
        customers.append((cid, name, city))
        segments[cid] = "low"
        cid += 1

    cursor.executemany("INSERT INTO customers VALUES(?,?,?)", customers)

    categories = {
        "Electronics": (8000, 60000),
        "Clothing": (500, 4000),
        "Home": (1000, 15000),
        "Sports": (700, 10000),
        "Accessories": (200, 2000)
    }

    products = []
    product_categories = {}

    pid = 1

    for cat in categories:
        low_price, high_price = categories[cat]

        for i in range(10):
            price = round(random.uniform(low_price, high_price), 2)
            products.append((pid, cat + " item " + str(i+1), cat, price))
            product_categories[pid] = cat
            pid += 1

    cursor.executemany("INSERT INTO products VALUES(?,?,?,?)", products)

    def random_date():
        delta = END_DATE - START_DATE
        while True:
            d = START_DATE + timedelta(days=random.randint(0, delta.days))
            if d.month == 2 and random.random() < 0.3:
                continue
            return d.strftime("%Y-%m-%d")

    def purchase_count(seg):
        if seg == "high":
            return random.randint(20, 35)
        elif seg == "medium":
            return random.randint(8, 15)
        else:
            return random.randint(1, 5)

    orders = []
    oid = 1

    for cid in segments:
        count = purchase_count(segments[cid])

        for i in range(count):

            pid = random.choice(products)[0]
            cat = product_categories[pid]

            if cat == "Electronics":
                qty = 1
            elif cat == "Accessories":
                qty = random.randint(2, 4)
            else:
                qty = random.randint(1, 3)

            orders.append((oid, cid, pid, qty, random_date()))
            oid += 1

    while len(orders) < MIN_ORDERS:

        cid = random.choice(list(segments.keys()))
        pid = random.choice(products)[0]
        cat = product_categories[pid]

        if cat == "Electronics":
            qty = 1
        elif cat == "Accessories":
            qty = random.randint(2, 4)
        else:
            qty = random.randint(1, 3)

        orders.append((oid, cid, pid, qty, random_date()))
        oid += 1

    cursor.executemany("INSERT INTO orders VALUES(?,?,?,?,?)", orders)

    conn.commit()
    conn.close()

    print("done")
    print("orders:", len(orders))

