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





# join_table_product_order=get_connection().execute("select * from products p \
#                             join orders o \
#                             on p.product_id=o.product_id").fetchall()

#join looks like this:


"""
p.id , p.name, p.category, p.price, o.id, o.customer_id, o.product_id, o.quantity, o.order_date
"""


