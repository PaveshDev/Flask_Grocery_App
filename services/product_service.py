"""
Product Service - Handles all product-related operations
Categories, products, inventory management, pricing
"""

try:
    from config.db_config import connect_db
except ImportError:
    from db_config import connect_db

from datetime import datetime


class ProductService:
    """Service class for product operations"""
    
    # ==================== CATEGORY FUNCTIONS ====================
    
    @staticmethod
    def get_all_categories():
        """Get all product categories"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT category_id, category_name, icon FROM categories ORDER BY category_name")
        categories = cursor.fetchall()
        db.close()
        return categories

    @staticmethod
    def get_categories_with_count():
        """Get all categories with item count in each"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT c.category_id, c.category_name, COUNT(p.product_id) as item_count
            FROM categories c
            LEFT JOIN products p ON c.category_id = p.category_id 
                AND (p.is_available = TRUE OR p.is_available IS NULL) 
                AND p.stock_quantity > 0
            GROUP BY c.category_id, c.category_name
            ORDER BY c.category_name
        """
        cursor.execute(query)
        categories = cursor.fetchall()
        db.close()
        return categories

    # ==================== PRODUCT RETRIEVAL FUNCTIONS ====================

    @staticmethod
    def get_products_by_category(category_id=None):
        """Get products by category or all products"""
        db = connect_db()
        cursor = db.cursor()
        
        if category_id:
            query = """
                SELECT p.product_id, p.name, p.description, p.image_path, 
                       p.unit_price, p.unit, p.stock_quantity, p.is_available,
                       p.discount_percent, c.category_name
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                WHERE p.category_id = %s AND p.is_available = TRUE
                ORDER BY p.name
            """
            cursor.execute(query, (category_id,))
        else:
            query = """
                SELECT p.product_id, p.name, p.description, p.image_path, 
                       p.unit_price, p.unit, p.stock_quantity, p.is_available,
                       p.discount_percent, c.category_name
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                WHERE p.is_available = TRUE
                ORDER BY c.category_name, p.name
            """
            cursor.execute(query)
        
        products = cursor.fetchall()
        db.close()
        return products

    @staticmethod
    def search_products(search_term):
        """Search products by name or description"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT p.product_id, p.name, p.description, p.image_path, 
                   p.unit_price, p.unit, p.stock_quantity, p.is_available,
                   p.discount_percent, c.category_name
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE (p.name LIKE %s OR p.description LIKE %s) 
            AND p.is_available = TRUE
            ORDER BY p.name
        """
        search_pattern = f"%{search_term}%"
        cursor.execute(query, (search_pattern, search_pattern))
        products = cursor.fetchall()
        db.close()
        return products

    @staticmethod
    def get_product_details(product_id):
        """Get detailed information about a product"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT p.product_id, p.name, p.description, p.image_path, 
                   p.unit_price, p.unit, p.stock_quantity, p.is_available,
                   p.discount_percent, c.category_name, c.category_id,
                   p.min_stock_level
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE p.product_id = %s
        """
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        db.close()
        return product

    @staticmethod
    def get_product_by_id_full(product_id):
        """Get full product details including dates for editing"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT product_id, name, unit_price, stock_quantity, unit, 
                   manufactured_date, expiry_date
            FROM products 
            WHERE product_id = %s
        """
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        db.close()
        return product

    @staticmethod
    def get_products_in_category(category_id):
        """Get all products in a specific category"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT product_id, name, stock_quantity, unit_price, unit, expiry_date
            FROM products 
            WHERE category_id = %s 
                AND (is_available = TRUE OR is_available IS NULL) 
                AND stock_quantity > 0
            ORDER BY name
        """
        cursor.execute(query, (category_id,))
        products = cursor.fetchall()
        db.close()
        return products

    # ==================== PRODUCT CREATION & MODIFICATION ====================

    @staticmethod
    def add_product(name, category_id, description, image_path, unit_price, unit, stock_quantity, min_stock_level=5):
        """Add a new product (Admin only)"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            INSERT INTO products (name, category_id, description, image_path, 
                                unit_price, unit, stock_quantity, min_stock_level, is_available)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        """
        
        values = (name, category_id, description, image_path, 
                  unit_price, unit, stock_quantity, min_stock_level)
        
        cursor.execute(query, values)
        db.commit()
        product_id = cursor.lastrowid
        db.close()
        return product_id

    @staticmethod
    def update_product(product_id, name, category_id, description, image_path, unit_price, unit, stock_quantity, min_stock_level):
        """Update product details (Admin only)"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            UPDATE products 
            SET name = %s, category_id = %s, description = %s, image_path = %s,
                unit_price = %s, unit = %s, stock_quantity = %s, min_stock_level = %s
            WHERE product_id = %s
        """
        cursor.execute(query, (name, category_id, description, image_path, 
                              unit_price, unit, stock_quantity, min_stock_level, product_id))
        db.commit()
        db.close()
        return True

    @staticmethod
    def update_product_details(product_id, name, category_id, description, image_path, unit_price, unit, stock_quantity, min_stock_level):
        """Wrapper for update_product - updates product details"""
        return ProductService.update_product(product_id, name, category_id, description, image_path, unit_price, unit, stock_quantity, min_stock_level)

    @staticmethod
    def delete_product(product_id):
        """Delete a product (Admin only)"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        db.commit()
        db.close()
        return True

    @staticmethod
    def delete_product_by_id(product_id):
        """Wrapper for delete_product - deletes product by ID"""
        return ProductService.delete_product(product_id)

    # ==================== PRODUCT STOCK & AVAILABILITY ====================

    @staticmethod
    def toggle_product_availability(product_id, is_available):
        """Enable/disable product (Admin only)"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE products SET is_available = %s WHERE product_id = %s", 
                      (is_available, product_id))
        db.commit()
        db.close()
        return True

    @staticmethod
    def update_product_stock(product_id, quantity_change):
        """Update product stock quantity"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE products 
            SET stock_quantity = stock_quantity + %s 
            WHERE product_id = %s
        """, (quantity_change, product_id))
        db.commit()
        db.close()
        return True

    @staticmethod
    def get_low_stock_products():
        """Get products with stock below minimum level"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM low_stock_products")
        products = cursor.fetchall()
        db.close()
        return products

    # ==================== PRODUCT ANALYSIS & STATISTICS ====================

    @staticmethod
    def calculate_discounted_price(unit_price, discount_percent):
        """Calculate final price after discount"""
        if discount_percent > 0:
            discount = (unit_price * discount_percent) / 100
            return unit_price - discount
        return unit_price

    @staticmethod
    def get_product_sold_count(product_id):
        """Get total units sold for a product (from all orders)"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT COALESCE(SUM(oi.quantity), 0) as total_sold
            FROM order_items oi
            WHERE oi.product_id = %s
        """
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        db.close()
        return result[0] if result else 0

    @staticmethod
    def get_inventory_stats():
        """Get inventory statistics including expiring soon and expired items"""
        db = connect_db()
        cursor = db.cursor()
        
        # Total items (count of products, not stock quantity)
        cursor.execute("SELECT COUNT(*) FROM products WHERE is_available = TRUE AND stock_quantity > 0")
        total_items = cursor.fetchone()[0]
        
        # Expiring soon (between today and 7 days from today)
        cursor.execute("""
            SELECT COUNT(*) FROM products 
            WHERE is_available = TRUE 
            AND expiry_date IS NOT NULL
            AND expiry_date > CURDATE() 
            AND expiry_date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
            AND stock_quantity > 0
        """)
        expiring_soon = cursor.fetchone()[0]
        
        # Expired items (past expiry date)
        cursor.execute("""
            SELECT COUNT(*) FROM products 
            WHERE is_available = TRUE 
            AND expiry_date IS NOT NULL
            AND expiry_date < CURDATE()
            AND stock_quantity > 0
        """)
        expired = cursor.fetchone()[0]
        
        db.close()
        return {
            'total_items': total_items,
            'expiring_soon': expiring_soon,
            'expired': expired
        }

    # ==================== EXPIRY MANAGEMENT ====================

    @staticmethod
    def get_expiring_soon_items():
        """Get items expiring within 7 days"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT product_id, name, stock_quantity, expiry_date, unit_price
            FROM products 
            WHERE is_available = TRUE 
            AND expiry_date IS NOT NULL
            AND expiry_date > CURDATE() 
            AND expiry_date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
            AND stock_quantity > 0
            ORDER BY expiry_date ASC
        """
        cursor.execute(query)
        items = cursor.fetchall()
        db.close()
        return items

    @staticmethod
    def get_expired_items():
        """Get expired items"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT product_id, name, stock_quantity, expiry_date, unit_price
            FROM products 
            WHERE is_available = TRUE 
            AND expiry_date IS NOT NULL
            AND expiry_date < CURDATE()
            AND stock_quantity > 0
            ORDER BY expiry_date DESC
        """
        cursor.execute(query)
        items = cursor.fetchall()
        db.close()
        return items

    @staticmethod
    def remove_expired_item(product_id):
        """Remove/delete expired item from inventory by setting stock to 0"""
        db = connect_db()
        cursor = db.cursor()
        
        query = "UPDATE products SET stock_quantity = 0 WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        db.commit()
        db.close()
        return True

    # ==================== INVENTORY VIEW FUNCTIONS ====================

    @staticmethod
    def get_inventory_by_category():
        """Get all items grouped by category with stock details"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT c.category_id, c.category_name, p.product_id, p.name, p.stock_quantity, 
                   p.unit_price, p.unit, p.expiry_date
            FROM categories c
            LEFT JOIN products p ON c.category_id = p.category_id AND p.is_available = TRUE
            ORDER BY c.category_name, p.name
        """
        cursor.execute(query)
        results = cursor.fetchall()
        db.close()
        
        # Group by category
        categories_dict = {}
        for row in results:
            cat_id, cat_name, prod_id, prod_name, stock, price, unit, expiry = row
            if cat_name not in categories_dict:
                categories_dict[cat_name] = {'id': cat_id, 'products': []}
            if prod_id:  # Only add if product exists
                categories_dict[cat_name]['products'].append({
                    'id': prod_id,
                    'name': prod_name,
                    'stock': stock,
                    'price': price,
                    'unit': unit,
                    'expiry': expiry
                })
        
        return categories_dict

    # ==================== LEGACY FUNCTIONS ====================

    @staticmethod
    def view_all_products():
        """Legacy function - returns all products"""
        return ProductService.get_products_by_category()
