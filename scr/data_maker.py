import random
import sqlite3 as sql

quantity = random.randint(1, 10)
order_date = f"{random.randint(2022, 2026)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

def quantity_maker(x=1, y=20):
    return random.randint(x, y)

def order_date_maker(start_year=2022, end_year=2026):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  
    if month in [1,2,3] :
       quantity = quantity_maker(1,10)
    elif month in [4,5,6] :
         quantity = quantity_maker(5,20)
    elif month in [10,11,12] :
         quantity = quantity_maker(5,25)
    else:
         quantity = quantity_maker(15,40)

    return {"year": year, "month": month, "day": day, "quantity": quantity}

def product_category_maker():
    categories = [
        "Electronics", 
        "Clothing",
        "Home " ,
        "Kitchen",
        "Books",
        "Toys",
        "Sports",
        "Beauty",
        "Automotive",
        "Grocery",
        "Health",
        "Garden",
        "Office",
        "Pet Supplies",
        "Baby Products",
        "Jewelry",
        "Music",
        "Movies",
        "Video Games",
        "Tools",
        "Outdoors",
        "Furniture",
        "Appliances",
        "Art",
          ]
    return random.choice(categories)

def customer_city_maker():
    cities = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
        "Austin",
        "Jacksonville",
        "Fort Worth",
        "Columbus",
        "Charlotte",
        "San Francisco",
        "Indianapolis",
        "Seattle",
        "Denver",
        "Washington"
    ]
    return random.choice(cities)

def customer_name_maker():
    first_names = [
        "John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Jessica",
        "James", "Mary", "William", "Linda", "Richard", "Barbara", "Joseph",
        "Susan", "Thomas", "Karen", "Charles", "Lisa"
    ]
    last_names = [
        "Smith", "Johnson", "Brown", "Taylor", "Anderson", "Thomas",
        "Jackson", "White", "Harris", "Martin", "Thompson",
        "Garcia", "Martinez", "Robinson", "Clark"
    ]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def make_customer_class():
    return {
        "name": customer_name_maker(),
        "city": customer_city_maker()
    }



with sql.connect("test.db") as con:
    cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS shet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    product_category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    order_date TEXT NOT NULL
)
""")

formatted_date = f"{order_date_maker()['year']}-{order_date_maker()['month']:02d}-{order_date_maker()['day']:02d}"

cur.execute("""
INSERT INTO shet (name, city, product_category, quantity, order_date)
VALUES (?, ?, ?, ?, ?)
""", (
    customer_name_maker(),
    customer_city_maker(),
    product_category_maker(),
    quantity_maker(),
    formatted_date
))

#cur.execute("""delete from shet""")


con.commit()