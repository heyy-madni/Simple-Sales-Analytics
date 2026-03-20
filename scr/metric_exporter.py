from database_manager import get_connection #type: ignore

def get_metrics(limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()

    def scalar(sql, params=()):
        row = cursor.execute(sql, params).fetchone()
        return row[0] if row and row[0] is not None else 0

    def rows(sql, params=()):
        return cursor.execute(sql, params).fetchall()

    customers_count = scalar("SELECT COUNT(*) FROM customers")
    products_count = scalar("SELECT COUNT(*) FROM products")
    orders_count = scalar("SELECT COUNT(*) FROM orders")

    total_revenue = scalar("""
        SELECT SUM(p.price * o.quantity)
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
    """)

    total_units = scalar("SELECT SUM(quantity) FROM orders")

    first_customers = rows(f"""
        SELECT customer_id, name, city
        FROM customers
        ORDER BY customer_id
        LIMIT {limit}
    """)

    top_products_by_price = rows("""
        SELECT name, category, price
        FROM products
        ORDER BY price DESC
        LIMIT ?
    """, (limit,))

    revenue_concentration_ratio = scalar("""
        SELECT
            (SELECT SUM(p.price * o.quantity)
             FROM orders o
                 JOIN products p ON p.product_id = o.product_id
                 JOIN customers c ON c.customer_id = o.customer_id
                 WHERE c.customer_id IN (
                     SELECT o2.customer_id
                     FROM orders o2
                         JOIN products p2 ON p2.product_id = o2.product_id
                     GROUP BY o2.customer_id
                     ORDER BY SUM(p2.price * o2.quantity) DESC
                     LIMIT 5
                 ))
            /
            (SELECT SUM(p.price * o.quantity)
             FROM orders o
                 JOIN products p ON p.product_id = o.product_id)
    """)



    conn.close()

    return {
        "customers_count": customers_count,
        "products_count": products_count,
        "total_orders": orders_count,
        "total_revenue": round(total_revenue, 2),
        "total_units_sold": total_units,
        "average_order_value": round(total_revenue / orders_count, 2) if orders_count else 0,
        "average_sale_price": round(total_revenue / total_units, 2) if total_units else 0,
        "first_customers": first_customers,
        "top_products_by_price": top_products_by_price,
        "revenue_concentration_ratio": revenue_concentration_ratio,

    }


def executive_snapshot():
    metrics = get_metrics()
    return {
        "Total Revenue": f"₹{metrics['total_revenue']:,}",
        "Total Orders": f"{metrics['total_orders']:,}",
        "Unique Customers": f"{metrics['customers_count']:,}",
        "Average Order Value": f"₹{metrics['average_order_value']:,}",
        "Average Units / Order": f"{round(metrics['total_units_sold'] / metrics['total_orders'], 2) if metrics['total_orders'] else 0}",
        "Revenue per Unit": f"₹{metrics['average_sale_price']:,}"
    }

print(f"monthly_growth_rate: {round(get_metrics()['monthly_growth_rate'] * 100, 2)}%")
print(f"Revenue Concentration Ratio (Top 5 Customers): {round(get_metrics()['revenue_concentration_ratio'] * 100, 2)}%")
print(f"Repeat Customer Rate: {round(get_metrics()['repeat_customer_rate'], 2)}%")



# total_orders: 26000
# total_revenue: 366563104.5
# total_units_sold: 51921
# average_order_value: 14098.58
# average_sale_price: 7060.02
# first_5_customers: [(1, 'ali khan', 'Ahmedabad'),
#  (2, 'Myra sayyid', 'Bangalore'),
#  (3, 'ali siddiqui', 'Delhi'),
#  (4, 'farhan mohammed', 'Mumbai'),
#  (5, 'madni ansari', 'Surat')]    
# top_products_by_price: [('Electronics item 6',
#  'Electronics', 58171.25),
#  ('Electronics item 10',
#  'Electronics', 48858.77),
#  ('Electronics item 1',
#  'Electronics', 48647.65),
#  ('Electronics item 9',
#  'Electronics', 48536.32),
#  ('Electronics item 5',
#  'Electronics', 38299.21)] 