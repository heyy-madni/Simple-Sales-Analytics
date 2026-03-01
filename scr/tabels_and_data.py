import random
import sqlite3 as sql
from pathlib import Path
from data_maker import  product_category_maker, order_date_maker, make_customer_class

#note i change values to 0
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_BASE_DIR = BASE_DIR / "database"
DATA_BASE_DIR.mkdir(parents=True, exist_ok=True)
FILE_DIR = DATA_BASE_DIR / "database.db"


def get_connection():
    con = sql.connect(FILE_DIR)
    con.execute("PRAGMA foreign_keys = ON")
    return con


def create_tables():
    with get_connection() as con:
        cur = con.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """)


def seed_customers(n=0):
    with get_connection() as con:
        cur = con.cursor()

        for _ in range(n):
            customer = make_customer_class()
            cur.execute(
                "INSERT INTO customers (name, city) VALUES (?, ?)",
                (customer["name"], customer["city"])
            )


def seed_products(n=0):
    with get_connection() as con:
        cur = con.cursor()

        for _ in range(n):
            category = product_category_maker()
            price = round(random.random() * 1000, 2)

            cur.execute(
                "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
                (f"{category} Product", category, price)
            )


def seed_orders(n=0):
    with get_connection() as con:
        cur = con.cursor()

        cur.execute("SELECT customer_id FROM customers")
        customers = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT product_id FROM products")
        products = [row[0] for row in cur.fetchall()]

        for _ in range(n):
            order_data = order_date_maker()

            date = f"{order_data['year']}-{order_data['month']:02d}-{order_data['day']:02d}"
            quantity = order_data["quantity"]

            cur.execute(
                "INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)",
                (random.choice(customers), random.choice(products), quantity, date)
            )


def data_bundel():
    customers_count=get_connection().execute("SELECT count(*) FROM customers").fetchone()[0]
    product_count=get_connection().execute("SELECT count(*) FROM products").fetchone()[0]
    orders_count=get_connection().execute("SELECT count(*) FROM orders").fetchone()[0]
    first_5_customers=get_connection().execute("SELECT * FROM customers LIMIT 5").fetchall() #check the data by inspect 
    
    
    
    
    return {
        "customers_count": customers_count,
        "products_count": product_count,
        "orders_count": orders_count,
        "first_5_customers": first_5_customers
    }


# join_table_product_order=get_connection().execute("select * from products p \
#                             join orders o \
#                             on p.product_id=o.product_id").fetchall()

#join looks like this:
"""
p.id , p.name, p.category, p.price, o.id, o.customer_id, o.product_id, o.quantity, o.order_date
"""



# metrics layer
total_revenue=get_connection().execute("SELECT sum(p.price*o.quantity) FROM products p JOIN orders o ON p.product_id = o.product_id").fetchone()[0]
total_orders=get_connection().execute("SELECT count(*) FROM orders").fetchone()[0]

def print_revenue_report():
    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_order_value": total_revenue/total_orders if total_orders > 0 else 0,
        "total_units_sold": get_connection().execute("SELECT sum(quantity) FROM orders").fetchone()[0]
    }






# for key, value in print_revenue_report().items():
#     print(f"{key}: {value}")
