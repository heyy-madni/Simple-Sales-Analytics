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


    revenue_by_product=get_connection().execute("""
        SELECT p.name, SUM(o.quantity * p.price) as total_revenue
        FROM products p
        JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.name
    """).fetchall()
    
    unit_sold_by_category=get_connection().execute("""
        SELECT p.category, SUM(o.quantity) as total_units
        FROM products p
        JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.category
    """).fetchall()
    

    top_5_products_by_revenue=get_connection().execute("""
        SELECT p.name, SUM(o.quantity * p.price) as total_revenue
        FROM products p
        JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.name
        ORDER BY total_revenue DESC
        LIMIT 5
    """).fetchall()
  


    conn.close()

    return {
        "customers count": customers_count,
        "products count": products_count,
        "total orders": orders_count,
        "total revenue": round(total_revenue, 2),
        "total units sold": total_units,
        "average_order_value": round(total_revenue / orders_count, 2) if orders_count else 0,
        "average sale price": round(total_revenue / total_units, 2) if total_units else 0,
        "first customers": first_customers,
        "estimated orders": round(total_revenue / (total_revenue / orders_count), 2) if orders_count else 0,
        "price to value_gap": round((total_revenue / total_units) - (total_revenue / orders_count), 2) if orders_count and total_units else 0,
        "revenue by category":revenue_by_product,
        "unit sold by category":unit_sold_by_category,
        "top 5 products by revenue":top_5_products_by_revenue
    }





def executive_snapshot():
    metrics = get_metrics()
    return {
        "Total Revenue": f"₹{metrics['total revenue']:,}",
        "Total Orders": f"{metrics['total orders']:,}",
        "Unique Customers": f"{metrics['customers count']:,}",
        "Average Order Value": f"₹{metrics['average order value']:,}",
        "Average Units / Order": f"{round(metrics['total units sold'] / metrics['total orders'], 2) if metrics['total orders'] else 0}",
        "Revenue per Unit": f"₹{metrics['average sale price']:,}"
    }



def row_to_dict(row, columns):
    return {col: row[idx] for idx, col in enumerate(columns)}




