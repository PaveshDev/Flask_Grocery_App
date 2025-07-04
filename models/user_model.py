import bcrypt

from db_config import connect_db

def register_user(username, password, email):
    db = connect_db()
    cursor = db.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        db.close()
        return False  # Username already exists

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert user with hashed password
    query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, hashed_password.decode('utf-8'), email))
    db.commit()
    db.close()
    return True

def login_user(username, password):
    db = connect_db()
    cursor = db.cursor()

    # Fetch user by username
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    db.close()

    # Verify user and password
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return user
    else:
        return None
