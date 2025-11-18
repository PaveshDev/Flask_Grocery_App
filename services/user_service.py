"""
User Service - Handles all user-related operations
Customer and Staff authentication, profile management
"""
import bcrypt
from datetime import datetime

try:
    from config.db_config import connect_db
except ImportError:
    from db_config import connect_db


class UserService:
    """Service class for user operations"""
    
    # ==================== CUSTOMER FUNCTIONS ====================
    
    @staticmethod
    def register_user(username, password, email, full_name='', phone='', address=''):
        """Register a new customer"""
        db = connect_db()
        cursor = db.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            db.close()
            return False, "Username already exists"
        
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            db.close()
            return False, "Email already exists"

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert user
        query = """
            INSERT INTO users (username, password, email, full_name, phone, address) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, hashed_password.decode('utf-8'), email, full_name, phone, address))
        db.commit()
        user_id = cursor.lastrowid
        db.close()
        return True, user_id

    @staticmethod
    def login_user(username, password):
        """Login customer"""
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s AND is_active = TRUE", (username,))
        user = cursor.fetchone()
        
        # Update last login
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            cursor.execute("UPDATE users SET last_login = %s WHERE user_id = %s", 
                          (datetime.now(), user[0]))
            db.commit()
            db.close()
            return user
        
        db.close()
        return None

    @staticmethod
    def update_user_profile(user_id, full_name, phone, address):
        """Update customer profile"""
        db = connect_db()
        cursor = db.cursor()
        
        query = """
            UPDATE users 
            SET full_name = %s, phone = %s, address = %s 
            WHERE user_id = %s
        """
        cursor.execute(query, (full_name, phone, address, user_id))
        db.commit()
        db.close()
        return True

    @staticmethod
    def get_user_info(user_id):
        """Get customer information"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        db.close()
        return user

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change customer password"""
        db = connect_db()
        cursor = db.cursor()
        
        # Get current password
        cursor.execute("SELECT password FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        
        if not result:
            db.close()
            return False, "User not found"
        
        # Verify old password
        if not bcrypt.checkpw(old_password.encode('utf-8'), result[0].encode('utf-8')):
            db.close()
            return False, "Incorrect old password"
        
        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Update password
        cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", 
                      (hashed_password.decode('utf-8'), user_id))
        db.commit()
        db.close()
        return True, "Password changed successfully"

    @staticmethod
    def update_username(user_id, new_username):
        """Update customer username"""
        db = connect_db()
        cursor = db.cursor()
        
        # Check if new username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s AND user_id != %s", (new_username, user_id))
        if cursor.fetchone():
            db.close()
            return False, "Username already exists"
        
        # Update username
        cursor.execute("UPDATE users SET username = %s WHERE user_id = %s", (new_username, user_id))
        db.commit()
        db.close()
        return True, "Username updated successfully"

    # ==================== STAFF FUNCTIONS ====================

    @staticmethod
    def login_staff(username, password):
        """Login staff/admin"""
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM staff WHERE username = %s AND is_active = TRUE", (username,))
        staff = cursor.fetchone()
        
        # Update last login
        if staff and bcrypt.checkpw(password.encode('utf-8'), staff[2].encode('utf-8')):
            cursor.execute("UPDATE staff SET last_login = %s WHERE staff_id = %s", 
                          (datetime.now(), staff[0]))
            db.commit()
            db.close()
            return staff
        
        db.close()
        return None

    @staticmethod
    def register_staff(username, password, email, full_name, phone='', role='staff'):
        """Register a new staff member (Admin only)"""
        db = connect_db()
        cursor = db.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM staff WHERE username = %s", (username,))
        if cursor.fetchone():
            db.close()
            return False, "Username already exists"

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert staff
        query = """
            INSERT INTO staff (username, password, email, full_name, phone, role) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, hashed_password.decode('utf-8'), email, full_name, phone, role))
        db.commit()
        staff_id = cursor.lastrowid
        db.close()
        return True, staff_id

    @staticmethod
    def get_staff_role(staff):
        """Get the role of a staff member"""
        if staff and len(staff) > 6:
            return staff[6]  # role is the 7th column
        return None

    @staticmethod
    def is_admin(staff):
        """Check if staff member is admin"""
        return UserService.get_staff_role(staff) == 'admin'

    @staticmethod
    def get_all_staff():
        """Get all staff members (Admin only)"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT staff_id, username, email, full_name, phone, role, is_active, created_at FROM staff ORDER BY role, username")
        staff_list = cursor.fetchall()
        db.close()
        return staff_list

    @staticmethod
    def toggle_staff_status(staff_id, is_active):
        """Enable/disable staff account (Admin only)"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE staff SET is_active = %s WHERE staff_id = %s", (is_active, staff_id))
        db.commit()
        db.close()
        return True

    @staticmethod
    def change_staff_password(staff_id, old_password, new_password):
        """Change staff password"""
        db = connect_db()
        cursor = db.cursor()
        
        # Get current password
        cursor.execute("SELECT password FROM staff WHERE staff_id = %s", (staff_id,))
        result = cursor.fetchone()
        
        if not result:
            db.close()
            return False, "Staff not found"
        
        # Verify old password
        if not bcrypt.checkpw(old_password.encode('utf-8'), result[0].encode('utf-8')):
            db.close()
            return False, "Incorrect old password"
        
        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Update password
        cursor.execute("UPDATE staff SET password = %s WHERE staff_id = %s", 
                      (hashed_password.decode('utf-8'), staff_id))
        db.commit()
        db.close()
        return True, "Password changed successfully"

    # ==================== HELPER FUNCTIONS ====================

    @staticmethod
    def get_user_role(user):
        """Get role of user - returns 'customer' for users"""
        return 'customer'

    @staticmethod
    def get_role(entity):
        """Get role of either user or staff"""
        if entity is None:
            return None
        # If it's a staff member (check by length or specific column)
        if len(entity) > 6:
            return UserService.get_staff_role(entity)
        # Otherwise it's a customer
        return UserService.get_user_role(entity)
