"""
Inventory Service - Handles all inventory batch tracking and stock management
Batch management, expiry date tracking, inventory statistics
"""
from datetime import datetime, date

try:
    from config.db_config import connect_db
except ImportError:
    from db_config import connect_db


class InventoryService:
    """Service class for inventory operations"""
    
    # ==================== BATCH MANAGEMENT ====================
    
    @staticmethod
    def add_inventory_batch(product_id, quantity_received, purchase_price, supplier_name, 
                           received_date, expiry_date, added_by_staff_id, batch_number='', notes=''):
        """Add new inventory batch (Admin only)"""
        db = connect_db()
        cursor = db.cursor()
        
        # Generate batch number if not provided
        if not batch_number:
            batch_number = f"BATCH-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        query = """
            INSERT INTO inventory (product_id, batch_number, quantity_received, quantity_remaining,
                                  purchase_price, supplier_name, received_date, expiry_date, 
                                  added_by, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (product_id, batch_number, quantity_received, quantity_received,
                              purchase_price, supplier_name, received_date, expiry_date, 
                              added_by_staff_id, notes))
        
        # Update product stock
        cursor.execute("""
            UPDATE products 
            SET stock_quantity = stock_quantity + %s 
            WHERE product_id = %s
        """, (quantity_received, product_id))
        
        db.commit()
        inventory_id = cursor.lastrowid
        db.close()
        return inventory_id

    @staticmethod
    def get_product_inventory(product_id):
        """Get all inventory batches for a product"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT i.inventory_id, i.batch_number, i.quantity_received, i.quantity_remaining,
                   i.purchase_price, i.supplier_name, i.received_date, i.expiry_date,
                   s.full_name as added_by_name, i.notes, i.created_at
            FROM inventory i
            JOIN staff s ON i.added_by = s.staff_id
            WHERE i.product_id = %s
            ORDER BY i.expiry_date ASC, i.received_date DESC
        """
        cursor.execute(query, (product_id,))
        batches = cursor.fetchall()
        db.close()
        return batches

    @staticmethod
    def get_all_inventory():
        """Get all inventory batches"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT i.inventory_id, p.name, i.batch_number, i.quantity_received, 
                   i.quantity_remaining, i.purchase_price, i.supplier_name, 
                   i.received_date, i.expiry_date
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            ORDER BY i.expiry_date ASC, i.received_date DESC
        """
        cursor.execute(query)
        batches = cursor.fetchall()
        db.close()
        return batches

    @staticmethod
    def update_inventory_quantity(inventory_id, quantity_change):
        """Update inventory batch quantity"""
        db = connect_db()
        cursor = db.cursor()
        
        cursor.execute("""
            UPDATE inventory 
            SET quantity_remaining = quantity_remaining + %s 
            WHERE inventory_id = %s
        """, (quantity_change, inventory_id))
        
        db.commit()
        db.close()
        return True

    # ==================== EXPIRY DATE TRACKING ====================

    @staticmethod
    def get_expiring_soon(days=7):
        """Get inventory batches expiring within specified days"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT i.inventory_id, p.name, i.batch_number, i.quantity_remaining,
                   i.expiry_date, DATEDIFF(i.expiry_date, CURDATE()) as days_until_expiry
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            WHERE i.expiry_date IS NOT NULL 
            AND i.quantity_remaining > 0
            AND DATEDIFF(i.expiry_date, CURDATE()) <= %s
            AND DATEDIFF(i.expiry_date, CURDATE()) >= 0
            ORDER BY i.expiry_date ASC
        """
        cursor.execute(query, (days,))
        batches = cursor.fetchall()
        db.close()
        return batches

    @staticmethod
    def get_expired_inventory():
        """Get expired inventory batches"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            SELECT i.inventory_id, p.name, i.batch_number, i.quantity_remaining,
                   i.expiry_date
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            WHERE i.expiry_date < CURDATE() 
            AND i.quantity_remaining > 0
            ORDER BY i.expiry_date DESC
        """
        cursor.execute(query)
        batches = cursor.fetchall()
        db.close()
        return batches

    @staticmethod
    def dispose_expired_inventory(inventory_id):
        """Mark expired inventory as disposed"""
        db = connect_db()
        cursor = db.cursor()
        
        # Get product_id and quantity
        cursor.execute("""
            SELECT product_id, quantity_remaining 
            FROM inventory 
            WHERE inventory_id = %s
        """, (inventory_id,))
        result = cursor.fetchone()
        
        if result:
            product_id, quantity = result
            
            # Update inventory to 0
            cursor.execute("""
                UPDATE inventory 
                SET quantity_remaining = 0, notes = CONCAT(IFNULL(notes, ''), ' [DISPOSED ON ', CURDATE(), ']')
                WHERE inventory_id = %s
            """, (inventory_id,))
            
            # Update product stock
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = stock_quantity - %s 
                WHERE product_id = %s
            """, (quantity, product_id))
            
            db.commit()
            db.close()
            return True
        
        db.close()
        return False

    # ==================== INVENTORY STATISTICS ====================

    @staticmethod
    def get_inventory_stats():
        """Get inventory statistics"""
        db = connect_db()
        cursor = db.cursor()
        
        stats = {}
        
        # Total inventory value (at purchase price)
        cursor.execute("""
            SELECT SUM(quantity_remaining * purchase_price) 
            FROM inventory 
            WHERE quantity_remaining > 0
        """)
        stats['total_value'] = cursor.fetchone()[0] or 0
        
        # Total inventory items
        cursor.execute("SELECT SUM(quantity_remaining) FROM inventory")
        stats['total_items'] = cursor.fetchone()[0] or 0
        
        # Expiring soon count
        cursor.execute("""
            SELECT COUNT(*) FROM inventory 
            WHERE expiry_date IS NOT NULL 
            AND quantity_remaining > 0
            AND DATEDIFF(expiry_date, CURDATE()) <= 7
            AND DATEDIFF(expiry_date, CURDATE()) >= 0
        """)
        stats['expiring_soon'] = cursor.fetchone()[0] or 0
        
        # Expired count
        cursor.execute("""
            SELECT COUNT(*) FROM inventory 
            WHERE expiry_date < CURDATE() 
            AND quantity_remaining > 0
        """)
        stats['expired'] = cursor.fetchone()[0] or 0
        
        db.close()
        return stats
