"""
Order Service - Handles all order and shopping cart operations
Cart management, order placement, notifications, order tracking
"""
from datetime import datetime

try:
    from config.db_config import connect_db
except ImportError:
    from db_config import connect_db


class OrderService:
    """Service class for order operations"""
    
    # ==================== SHOPPING CART FUNCTIONS ====================
    
    @staticmethod
    def add_to_cart(user_id, product_id, quantity):
        """Add item to shopping cart"""
        db = connect_db()
        cursor = db.cursor()
        
        # Check stock availability
        cursor.execute("SELECT stock_quantity FROM products WHERE product_id = %s", (product_id,))
        result = cursor.fetchone()
        
        if not result or result[0] < quantity:
            db.close()
            return False, "Insufficient stock"
        
        # Check if item already in cart
        cursor.execute("""
            SELECT cart_id, quantity FROM shopping_cart 
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        existing = cursor.fetchone()
        
        if existing:
            # Update quantity
            new_quantity = existing[1] + quantity
            cursor.execute("""
                UPDATE shopping_cart 
                SET quantity = %s 
                WHERE cart_id = %s
            """, (new_quantity, existing[0]))
        else:
            # Add new item
            cursor.execute("""
                INSERT INTO shopping_cart (user_id, product_id, quantity) 
                VALUES (%s, %s, %s)
            """, (user_id, product_id, quantity))
        
        db.commit()
        db.close()
        return True, "Added to cart"

    @staticmethod
    def get_cart_items(user_id):
        """Get all items in user's cart"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT sc.cart_id, sc.product_id, p.name, p.image_path, 
                   p.unit_price, sc.quantity, (p.unit_price * sc.quantity) as subtotal,
                   p.stock_quantity, p.discount_percent
            FROM shopping_cart sc
            JOIN products p ON sc.product_id = p.product_id
            WHERE sc.user_id = %s
            ORDER BY sc.added_at DESC
        """
        cursor.execute(query, (user_id,))
        items = cursor.fetchall()
        db.close()
        return items

    @staticmethod
    def update_cart_quantity(cart_id, quantity):
        """Update cart item quantity"""
        db = connect_db()
        cursor = db.cursor()
        
        if quantity <= 0:
            cursor.execute("DELETE FROM shopping_cart WHERE cart_id = %s", (cart_id,))
        else:
            cursor.execute("UPDATE shopping_cart SET quantity = %s WHERE cart_id = %s", 
                          (quantity, cart_id))
        
        db.commit()
        db.close()
        return True

    @staticmethod
    def remove_from_cart(cart_id):
        """Remove item from cart"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM shopping_cart WHERE cart_id = %s", (cart_id,))
        db.commit()
        db.close()
        return True

    @staticmethod
    def clear_cart(user_id):
        """Clear all items from cart"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM shopping_cart WHERE user_id = %s", (user_id,))
        db.commit()
        db.close()
        return True

    @staticmethod
    def get_cart_total(user_id):
        """Get cart total amount"""
        db = connect_db()
        cursor = db.cursor()
        
        cursor.execute("""
            SELECT SUM(p.unit_price * sc.quantity) 
            FROM shopping_cart sc
            JOIN products p ON sc.product_id = p.product_id
            WHERE sc.user_id = %s
        """, (user_id,))
        result = cursor.fetchone()
        db.close()
        return result[0] if result[0] else 0.0

    # ==================== ORDER FUNCTIONS ====================

    @staticmethod
    def place_order(user_id, delivery_address, delivery_phone, payment_method='cash'):
        """Place order from cart"""
        db = connect_db()
        cursor = db.cursor()
        
        # Get cart items
        cursor.execute("""
            SELECT sc.product_id, sc.quantity, p.unit_price, p.stock_quantity
            FROM shopping_cart sc
            JOIN products p ON sc.product_id = p.product_id
            WHERE sc.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        
        if not cart_items:
            db.close()
            return False, "Cart is empty"
        
        # Check stock for all items
        for product_id, quantity, price, stock in cart_items:
            if stock < quantity:
                db.close()
                return False, f"Insufficient stock for product ID {product_id}"
        
        # Calculate total
        total_amount = sum(item[1] * item[2] for item in cart_items)
        final_amount = total_amount  # Same as total since no discounts
        
        # Generate order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create order
        cursor.execute("""
            INSERT INTO orders (user_id, order_number, total_amount, final_amount,
                               payment_method, delivery_address, delivery_phone, order_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
        """, (user_id, order_number, total_amount, final_amount,
              payment_method, delivery_address, delivery_phone))
        
        order_id = cursor.lastrowid
        
        # Add order items and update stock
        for product_id, quantity, price, stock in cart_items:
            # Get product name
            cursor.execute("SELECT name FROM products WHERE product_id = %s", (product_id,))
            product_name = cursor.fetchone()[0]
            
            subtotal = quantity * price
            
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, quantity, 
                                       unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (order_id, product_id, product_name, quantity, price, subtotal))
            
            # Update stock
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = stock_quantity - %s 
                WHERE product_id = %s
            """, (quantity, product_id))
        
        # Create notification
        OrderService._create_notification(cursor, user_id, 'order_placed', 
                           'Order Placed Successfully!',
                           f'Your order {order_number} has been placed successfully. Total: {final_amount:.2f}',
                           order_id)
        
        # Clear cart
        cursor.execute("DELETE FROM shopping_cart WHERE user_id = %s", (user_id,))
        
        db.commit()
        db.close()
        return True, f"Order {order_number} placed successfully!"

    @staticmethod
    def get_user_orders(user_id, limit=None):
        """Get user's order history"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT order_id, order_number, total_amount, discount_amount, final_amount,
                   payment_method, payment_status, order_status, delivery_address,
                   order_date, delivered_at
            FROM orders
            WHERE user_id = %s
            ORDER BY order_date DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (user_id,))
        orders = cursor.fetchall()
        db.close()
        return orders

    @staticmethod
    def get_order_details(order_id):
        """Get detailed information about an order"""
        db = connect_db()
        cursor = db.cursor()
        
        # Get order info
        cursor.execute("""
            SELECT o.order_id, o.order_number, o.total_amount, o.discount_amount, o.final_amount,
                   o.payment_method, o.payment_status, o.order_status, o.delivery_address,
                   o.delivery_phone, o.order_date, o.confirmed_at, o.delivered_at,
                   u.username, u.full_name, u.email
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            WHERE o.order_id = %s
        """, (order_id,))
        order = cursor.fetchone()
        
        # Get order items
        cursor.execute("""
            SELECT product_id, product_name, quantity, unit_price, discount_percent, subtotal
            FROM order_items
            WHERE order_id = %s
        """, (order_id,))
        items = cursor.fetchall()
        
        db.close()
        return order, items

    @staticmethod
    def get_all_orders(status=None, limit=None):
        """Get all orders (Admin only)"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT o.order_id, o.order_number, u.username, u.full_name,
                   o.final_amount, o.payment_status, o.order_status, o.order_date
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
        """
        
        if status:
            query += f" WHERE o.order_status = '{status}'"
        
        query += " ORDER BY o.order_date DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        orders = cursor.fetchall()
        db.close()
        return orders

    @staticmethod
    def update_order_status(order_id, new_status):
        """Update order status (Admin only)"""
        db = connect_db()
        cursor = db.cursor()
        
        cursor.execute("UPDATE orders SET order_status = %s WHERE order_id = %s", 
                      (new_status, order_id))
        
        # Get user_id for notification
        cursor.execute("SELECT user_id, order_number FROM orders WHERE order_id = %s", (order_id,))
        user_id, order_number = cursor.fetchone()
        
        # Create notification based on status
        notification_messages = {
            'confirmed': ('Order Confirmed', f'Your order {order_number} has been confirmed!'),
            'processing': ('Order Processing', f'Your order {order_number} is being processed.'),
            'shipped': ('Order Shipped', f'Your order {order_number} has been shipped!'),
            'delivered': ('Order Delivered', f'Your order {order_number} has been delivered. Thank you!')
        }
        
        if new_status in notification_messages:
            title, message = notification_messages[new_status]
            OrderService._create_notification(cursor, user_id, f'order_{new_status}', title, message, order_id)
        
        # Update confirmed_at or delivered_at
        if new_status == 'confirmed':
            cursor.execute("UPDATE orders SET confirmed_at = %s WHERE order_id = %s", 
                          (datetime.now(), order_id))
        elif new_status == 'delivered':
            cursor.execute("UPDATE orders SET delivered_at = %s WHERE order_id = %s", 
                          (datetime.now(), order_id))
        
        db.commit()
        db.close()
        return True

    # ==================== NOTIFICATION FUNCTIONS ====================

    @staticmethod
    def _create_notification(cursor, user_id, notif_type, title, message, order_id=None):
        """Create a notification for user (internal method using passed cursor)"""
        cursor.execute("""
            INSERT INTO notifications (user_id, type, title, message, order_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, notif_type, title, message, order_id))

    @staticmethod
    def get_user_notifications(user_id, unread_only=False):
        """Get user's notifications"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT notification_id, type, title, message, order_id, is_read, created_at
            FROM notifications
            WHERE user_id = %s
        """
        
        if unread_only:
            query += " AND is_read = FALSE"
        
        query += " ORDER BY created_at DESC LIMIT 50"
        
        cursor.execute(query, (user_id,))
        notifications = cursor.fetchall()
        db.close()
        return notifications

    @staticmethod
    def mark_notification_read(notification_id):
        """Mark notification as read"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE notifications SET is_read = TRUE WHERE notification_id = %s", 
                      (notification_id,))
        db.commit()
        db.close()
        return True

    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM notifications WHERE user_id = %s AND is_read = FALSE", 
                      (user_id,))
        count = cursor.fetchone()[0]
        db.close()
        return count

    # ==================== LEGACY COMPATIBILITY ====================

    @staticmethod
    def get_all_admin_orders():
        """Get all orders for admin view with customer info"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT o.order_id, o.user_id, u.full_name, u.phone, o.order_date, 
                   o.total_amount, o.delivery_address, COUNT(oi.order_item_id) as item_count
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY o.order_id, o.user_id, u.full_name, u.phone, o.order_date, o.total_amount, o.delivery_address
            ORDER BY o.order_date DESC
        """
        cursor.execute(query)
        orders = cursor.fetchall()
        db.close()
        return orders

    @staticmethod
    def view_orders(user_id):
        """Legacy function for backward compatibility"""
        orders = OrderService.get_user_orders(user_id)
        
        # Get items for all orders
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT oi.order_id, oi.product_name, oi.quantity
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            WHERE o.user_id = %s
            ORDER BY o.order_date DESC
        """, (user_id,))
        items = cursor.fetchall()
        db.close()
        
        return orders, items
