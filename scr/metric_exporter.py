from database_manager import get_connection



def get_metrics(limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()

    def query(sql, params=()):
        return cursor.execute(sql, params).fetchone()[0]

    def queryall(sql, params=()):
        return cursor.execute(sql, params).fetchall()

    customers_count = query("SELECT COUNT(*) FROM customers")
    products_count = query("SELECT COUNT(*) FROM products")
    orders_count = query("SELECT COUNT(*) FROM orders")

    total_revenue = query("""
        SELECT COALESCE(SUM(p.price * o.quantity), 0)
        FROM products p
        JOIN orders o ON p.product_id = o.product_id
    """)

    total_units = query("SELECT COALESCE(SUM(quantity), 0) FROM orders")

    first_5_customers_raw = queryall("SELECT * FROM customers LIMIT 5")
    top_sale_raw = queryall("""
        SELECT name, price
        FROM products
        ORDER BY price DESC
        LIMIT ?
    """, (limit,))

    return {
        "total_revenue": total_revenue,
        "total_orders": orders_count,
        "total_units_sold": total_units,
        "average_order_value": total_revenue / orders_count if orders_count else 0,
        "average_sale_price": total_revenue / total_units if total_units else 0,
        "customers_count": customers_count,
        "products_count": products_count,
        "first_5_customers": first_5_customers_raw,
        "top_sale": top_sale_raw,
    }



total=(get_metrics()["total_revenue"])
orc=get_metrics()["total_orders"]


print(f"Total Revenue: ${total:.2f}, Total Orders: {orc}")