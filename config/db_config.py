import mysql.connector

def connect_db():
    """Connect to the grocery_app_db database"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",   # 🔁 Replace this with your actual MySQL root password
        database="grocery_app_db"
    )

def get_db_connection():
    """Alternative connection method with error handling"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="grocery_app_db",
            autocommit=False
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None
