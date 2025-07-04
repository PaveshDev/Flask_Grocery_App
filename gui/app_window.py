import tkinter as tk
from tkinter import messagebox
from models.user_model import register_user, login_user
from models.product_model import view_all_products, delete_product, update_product, add_product
from models.order_model import add_to_cart, get_cart_items, place_order


class GroceryAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery App")
        self.root.geometry("400x400")
        self.user = None
        self.login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Login", font=("Arial", 20)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_screen).pack()

    def register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Register", font=("Arial", 20)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.reg_username = tk.Entry(self.root)
        self.reg_username.pack()

        tk.Label(self.root, text="Password").pack()
        self.reg_password = tk.Entry(self.root, show="*")
        self.reg_password.pack()

        tk.Label(self.root, text="Email").pack()
        self.reg_email = tk.Entry(self.root)
        self.reg_email.pack()

        tk.Button(self.root, text="Submit", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def register(self):
        uname = self.reg_username.get()
        pwd = self.reg_password.get()
        email = self.reg_email.get()

        if register_user(uname, pwd, email):
            messagebox.showinfo("Success", "Registered successfully!")
            self.login_screen()
        else:
            messagebox.showerror("Error", "Username already exists.")

    def login(self):
        uname = self.username_entry.get()
        pwd = self.password_entry.get()

        user = login_user(uname, pwd)
        if user:
            self.user = user
            messagebox.showinfo("Welcome", f"Welcome {user[1]}!")
            if user[1].lower() == "admin":
                self.admin_dashboard()
            else:
                self.customer_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def customer_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome {self.user[1]}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="View Products", command=self.view_products).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)

    def admin_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Admin Panel - {self.user[1]}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Product Management", command=self.view_products).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)

    def view_products(self):
        self.clear_screen()
        tk.Label(self.root, text="All Products", font=("Arial", 16)).pack(pady=10)

        products = view_all_products()
        for p in products:
            product_info = f"ID: {p[0]} | Name: {p[1]} | Price: {p[3]} | Stock: {p[4]}"
            tk.Label(self.root, text=product_info).pack()

        tk.Button(self.root, text="Back", command=self.customer_dashboard if self.user[1].lower() != "admin" else self.admin_dashboard).pack(pady=10)

    def add_to_cart_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Available Products", font=("Arial", 16)).pack(pady=10)

        products = view_all_products()
        for p in products:
            frame = tk.Frame(self.root)
            frame.pack(pady=2)

            tk.Label(frame, text=f"{p[1]} | ₹{p[3]} | Stock: {p[4]}").pack(side=tk.LEFT)

            qty_var = tk.IntVar(value=1)
            tk.Entry(frame, textvariable=qty_var, width=3).pack(side=tk.LEFT, padx=5)

            tk.Button(frame, text="Add to Cart",
                      command=lambda pid=p[0], qty=qty_var: self.add_to_cart(pid, qty)).pack(side=tk.LEFT)

        tk.Button(self.root, text="View Cart", command=self.view_cart).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.customer_dashboard).pack()

    def add_to_cart(self, product_id, qty_var):
        try:
            qty = int(qty_var.get())
            if qty <= 0:
                raise ValueError
            add_to_cart(product_id, qty)
            messagebox.showinfo("Success", f"Added {qty} item(s) to cart.")
        except:
            messagebox.showerror("Error", "Invalid quantity.")

    def view_cart(self):
        self.clear_screen()
        tk.Label(self.root, text="🛒 Your Cart", font=("Arial", 16)).pack(pady=10)

        items = get_cart_items()
        if not items:
            tk.Label(self.root, text="Cart is empty").pack()
        else:
            for item in items:
                tk.Label(self.root, text=f"Product ID: {item[0]} | Quantity: {item[1]}").pack()

            tk.Button(self.root, text="Checkout", command=self.checkout).pack(pady=10)

        tk.Button(self.root, text="Back", command=self.add_to_cart_screen).pack()

    def checkout(self):
        success, msg = place_order(self.user[0])
        if success:
            messagebox.showinfo("Order Placed", msg)
            self.customer_dashboard()
        else:
            messagebox.showerror("Failed", msg)

    def customer_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome {self.user[1]}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="🔎 Search / Filter Products", command=self.search_products_screen).pack(pady=5)
        tk.Button(self.root, text="View Products", command=self.view_products).pack(pady=5)
        tk.Button(self.root, text="🛒 Shop Now", command=self.add_to_cart_screen).pack(pady=5)
        tk.Button(self.root, text="📜 Order History", command=self.view_order_history).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)

    def admin_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Admin Panel - {self.user[1]}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="🔎 Search / Filter Products", command=self.search_products_screen).pack(pady=5)
        tk.Button(self.root, text="➕ Add Product", command=self.add_product_screen).pack(pady=5)
        tk.Button(self.root, text="📝 Update Product", command=self.update_product_screen).pack(pady=5)
        tk.Button(self.root, text="🗑 Delete Product", command=self.delete_product_screen).pack(pady=5)
        tk.Button(self.root, text="📋 View Products", command=self.view_products).pack(pady=5)
        tk.Button(self.root, text="📦 View All Orders", command=self.view_all_orders).pack(pady=5)
        tk.Button(self.root, text="📊 Dashboard Summary", command=self.view_summary).pack(pady=5)
        tk.Button(self.root, text="🔙 Logout", command=self.login_screen).pack(pady=10)

    def add_product_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Add New Product", font=("Arial", 16)).pack(pady=10)

        entries = {}
        for label in ["Name", "Category", "Price", "Stock"]:
            tk.Label(self.root, text=label).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[label.lower()] = entry

        def submit():
            try:
                name = entries["name"].get()
                category = entries["category"].get()
                price = float(entries["price"].get())
                stock = int(entries["stock"].get())
                add_product(name, category, price, stock)
                messagebox.showinfo("Success", "Product added!")
                self.admin_dashboard()
            except:
                messagebox.showerror("Error", "Invalid input.")

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack()

    def update_product_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Update Product", font=("Arial", 16)).pack(pady=10)

        entries = {}
        for label in ["Product ID", "New Name", "New Category", "New Price", "New Stock"]:
            tk.Label(self.root, text=label).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[label.lower()] = entry

        def submit():
            try:
                pid = int(entries["product id"].get())
                name = entries["new name"].get()
                category = entries["new category"].get()
                price = float(entries["new price"].get())
                stock = int(entries["new stock"].get())
                update_product(pid, name, category, price, stock)
                messagebox.showinfo("Success", "Product updated!")
                self.admin_dashboard()
            except:
                messagebox.showerror("Error", "Invalid input.")

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack()

    def delete_product_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Delete Product", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Product ID").pack()
        entry = tk.Entry(self.root)
        entry.pack()

        def submit():
            try:
                pid = int(entry.get())
                delete_product(pid)
                messagebox.showinfo("Deleted", "Product deleted!")
                self.admin_dashboard()
            except:
                messagebox.showerror("Error", "Invalid Product ID.")

        tk.Button(self.root, text="Delete", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack()

    def view_order_history(self):
        from models.order_model import view_orders
        self.clear_screen()
        tk.Label(self.root, text="📜 Your Order History", font=("Arial", 16)).pack(pady=10)

        orders, items = view_orders(self.user[0])

        if not orders:
            tk.Label(self.root, text="You have no orders yet.").pack(pady=10)
        else:
            for o in orders:
                tk.Label(self.root, text=f"Order ID: {o[0]} | Total: ₹{o[2]} | Date: {o[3]}",
                         font=("Arial", 10, "bold")).pack(pady=2)

                for i in items:
                    if i[0] == o[0]:  # Match order ID
                        tk.Label(self.root, text=f" - Product: {i[1]} | Quantity: {i[2]}").pack()

        tk.Button(self.root, text="Back", command=self.customer_dashboard).pack(pady=10)

    def view_all_orders(self):
        self.clear_screen()
        tk.Label(self.root, text="📦 All Orders", font=("Arial", 16)).pack(pady=10)

        from db_config import connect_db
        db = connect_db()
        cursor = db.cursor()

        # ✅ Correct SQL with actual column names
        cursor.execute("""
                       SELECT o.order_id, u.username, o.total_price, o.order_date
                       FROM orders o
                                JOIN users u ON o.user_id = u.user_id
                       ORDER BY o.order_date DESC
                       """)
        orders = cursor.fetchall()

        cursor.execute("""
                       SELECT oi.order_id, p.name, oi.quantity
                       FROM order_items oi
                                JOIN products p ON oi.product_id = p.product_id
                       """)
        items = cursor.fetchall()

        db.close()

        if not orders:
            tk.Label(self.root, text="No orders found.").pack()
        else:
            for o in orders:
                tk.Label(self.root, text=f"Order ID: {o[0]} | User: {o[1]} | ₹{o[2]} | {o[3]}",
                         font=("Arial", 10, "bold")).pack(pady=2)
                for i in items:
                    if i[0] == o[0]:
                        tk.Label(self.root, text=f"   • {i[1]} x {i[2]}").pack()

        tk.Button(self.root, text="🔙 Back", command=self.admin_dashboard).pack(pady=10)

    def view_summary(self):
        self.clear_screen()
        tk.Label(self.root, text="📊 Dashboard Summary", font=("Arial", 16)).pack(pady=10)

        from db_config import connect_db
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]

        cursor.execute("SELECT name, stock FROM products WHERE stock < 5")
        low_stock_items = cursor.fetchall()

        db.close()

        # Display Summary
        tk.Label(self.root, text=f"👥 Total Users: {user_count}", font=("Arial", 12)).pack(pady=2)
        tk.Label(self.root, text=f"📦 Total Products: {product_count}", font=("Arial", 12)).pack(pady=2)
        tk.Label(self.root, text=f"🧾 Total Orders: {order_count}", font=("Arial", 12)).pack(pady=2)

        # Low stock section
        if low_stock_items:
            tk.Label(self.root, text="⚠️ Low Stock Items (<5)", font=("Arial", 12, "bold")).pack(pady=5)
            for item in low_stock_items:
                tk.Label(self.root, text=f"{item[0]} - Only {item[1]} left").pack()
        else:
            tk.Label(self.root, text="✅ All items are sufficiently stocked.").pack(pady=5)

        tk.Button(self.root, text="🔙 Back", command=self.admin_dashboard).pack(pady=10)

    def search_products_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🔎 Search / Filter Products", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Search by Name:").pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack(pady=5)

        tk.Label(self.root, text="Filter by Category:").pack()
        category_var = tk.StringVar()
        category_dropdown = tk.OptionMenu(self.root, category_var, "All")  # Placeholder; updated below
        category_dropdown.pack(pady=5)

        result_box = tk.Text(self.root, width=60, height=15)
        result_box.pack(pady=10)

        def search():
            name_filter = name_entry.get()
            category_filter = category_var.get()

            from db_config import connect_db
            db = connect_db()
            cursor = db.cursor()

            query = "SELECT * FROM products WHERE 1"
            params = []

            if name_filter:
                query += " AND name LIKE %s"
                params.append(f"%{name_filter}%")
            if category_filter != "All":
                query += " AND category = %s"
                params.append(category_filter)

            cursor.execute(query, params)
            results = cursor.fetchall()
            db.close()

            result_box.delete(1.0, tk.END)
            if not results:
                result_box.insert(tk.END, "No products found.\n")
            else:
                for p in results:
                    result_box.insert(tk.END,
                                      f"ID: {p[0]} | Name: {p[1]} | Category: {p[2]} | Price: ₹{p[3]} | Stock: {p[4]}\n")

        tk.Button(self.root, text="Search", command=search).pack(pady=5)
        tk.Button(self.root, text="🔙 Back", command=self.admin_dashboard).pack(pady=10)

        # Populate category dropdown
        from db_config import connect_db
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT category FROM products")
        categories = cursor.fetchall()
        db.close()

        menu = category_dropdown["menu"]
        menu.delete(0, "end")
        menu.add_command(label="All", command=lambda: category_var.set("All"))
        for cat in categories:
            menu.add_command(label=cat[0], command=lambda c=cat[0]: category_var.set(c))
        category_var.set("All")

