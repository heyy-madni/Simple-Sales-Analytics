from database_manager import get_connection



def get_metrics(limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()

    def scalar(sql, params=()):
        row = cursor.execute(sql, params).fetchone()
        return row[0] if row and row[0] is not None else 0

    def rows(sql, params=()):
        return cursor.execute(sql, params).fetchall()

    # Basic counts
    customers_count = scalar("SELECT COUNT(*) FROM customers")
    products_count = scalar("SELECT COUNT(*) FROM products")
    orders_count = scalar("SELECT COUNT(*) FROM orders")

    # Revenue + Units
    total_revenue = scalar("""
        SELECT SUM(p.price * o.quantity)
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
    """)

    total_units = scalar("SELECT SUM(quantity) FROM orders")

    # Samples
    first_customers = rows("""
        SELECT customer_id, name, city
        FROM customers
        ORDER BY customer_id
        LIMIT 5
    """)

    top_products_by_price = rows("""
        SELECT name, category, price
        FROM products
        ORDER BY price DESC
        LIMIT ?
    """, (limit,))

    conn.close()

    return {
        "customers_count": customers_count,
        "products_count": products_count,
        "total_orders": orders_count,

        "total_revenue": round(total_revenue, 2),
        "total_units_sold": total_units,

        "average_order_value": round(total_revenue / orders_count, 2) if orders_count else 0,
        "average_sale_price": round(total_revenue / total_units, 2) if total_units else 0,

        "first_5_customers": first_customers,
        "top_products_by_price": top_products_by_price,
    }



total=(get_metrics()["total_revenue"])
orc=get_metrics()["total_orders"]


print(f"Total Revenue: ${total:.2f}, Total Orders: {orc}")