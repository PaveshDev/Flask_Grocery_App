from db_config import connect_db

try:
    db = connect_db()
    print("✅ Connection successful!")
    db.close()
except Exception as e:
    print("❌ Connection failed:", e)
