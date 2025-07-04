import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",   # 🔁 Replace this with your actual MySQL root password
        database="grocery_db"
    )
