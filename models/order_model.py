from db_config import connect_db
from datetime import datetime

cart = []  # global cart for current session

def add_to_cart(product_id, quantity):
    cart.append((product_id, quantity))

def get_cart_items():
    return cart

def clear_cart():
    cart.clear()

def place_order(user_id):
    if not cart:
        return False, "Cart is empty."

    db = connect_db()
    cursor = db.cursor()

    total_price = 0

    # Calculate total price
    for product_id, quantity in cart:
        cursor.execute("SELECT price, stock FROM products WHERE product_id = %s", (product_id,))
        result = cursor.fetchone()
        if not result or result[1] < quantity:
            db.close()
            return False, f"Product ID {product_id} has insufficient stock."
        total_price += result[0] * quantity

    # Insert into orders table
    order_date = datetime.now()
    cursor.execute("INSERT INTO orders (user_id, total_price, order_date) VALUES (%s, %s, %s)",
                   (user_id, total_price, order_date))
    order_id = cursor.lastrowid

    # Insert into order_items table
    for product_id, quantity in cart:
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                       (order_id, product_id, quantity))
        # Reduce stock
        cursor.execute("UPDATE products SET stock = stock - %s WHERE product_id = %s", (quantity, product_id))

    db.commit()
    db.close()
    clear_cart()
    return True, "Order placed successfully!"

def view_orders(user_id):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY order_date DESC", (user_id,))
    orders = cursor.fetchall()

    cursor.execute("""
        SELECT o.order_id, p.name, oi.quantity
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.user_id = %s
        ORDER BY o.order_id DESC
    """, (user_id,))
    items = cursor.fetchall()

    db.close()
    return orders, items
