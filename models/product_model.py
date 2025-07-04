from db_config import connect_db

def add_product(name, category, price, stock):
    db = connect_db()
    cursor = db.cursor()
    query = "INSERT INTO products (name, category, price, stock) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, category, price, stock))
    db.commit()
    db.close()

def view_all_products():
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    products = cursor.fetchall()
    db.close()
    return products

def update_product(product_id, name, category, price, stock):
    db = connect_db()
    cursor = db.cursor()
    query = "UPDATE products SET name=%s, category=%s, price=%s, stock=%s WHERE product_id=%s"
    cursor.execute(query, (name, category, price, stock, product_id))
    db.commit()
    db.close()

def delete_product(product_id):
    db = connect_db()
    cursor = db.cursor()
    query = "DELETE FROM products WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    db.commit()
    db.close()
