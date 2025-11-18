import tkinter as tk
from tkinter import messagebox, ttk
from models.user_model import register_user, login_user, get_user_role
from models.product_model import view_all_products, delete_product, update_product, add_product
from models.order_model import add_to_cart, get_cart_items, place_order


class GroceryAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery App")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.user = None
        self.user_role = None
        
        # Color scheme
        self.colors = {
            'primary': '#2196F3',
            'success': '#4CAF50',
            'danger': '#f44336',
            'warning': '#FF9800',
            'bg': '#f5f5f5',
            'card': '#ffffff',
            'text': '#333333',
            'text_light': '#666666'
        }
        
        self.login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_styled_button(self, parent, text, command, color='primary', width=20):
        """Create a styled button with modern look"""
        btn_color = self.colors.get(color, self.colors['primary'])
        btn = tk.Button(
            parent, 
            text=text, 
            command=command,
            bg=btn_color,
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            width=width,
            cursor='hand2'
        )
        return btn

    def create_styled_entry(self, parent, show=None):
        """Create a styled entry widget"""
        entry = tk.Entry(
            parent,
            font=('Arial', 11),
            relief=tk.SOLID,
            borderwidth=1,
            show=show
        )
        return entry

    def create_label(self, parent, text, font_size=11, bold=False):
        """Create a styled label"""
        font_style = ('Arial', font_size, 'bold' if bold else 'normal')
        label = tk.Label(
            parent,
            text=text,
            font=font_style,
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        return label

    def login_screen(self):
        self.clear_screen()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Center card
        card = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=2)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=450)

        tk.Label(
            card, 
            text="🛒 Grocery App", 
            font=("Arial", 24, "bold"),
            bg=self.colors['card'],
            fg=self.colors['primary']
        ).pack(pady=20)
        
        tk.Label(
            card, 
            text="Login to Continue", 
            font=("Arial", 14),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack(pady=5)

        # Username
        tk.Label(card, text="Username", bg=self.colors['card'], font=('Arial', 10)).pack(pady=(20, 5))
        self.username_entry = self.create_styled_entry(card)
        self.username_entry.pack(pady=5, padx=40, fill=tk.X)

        # Password
        tk.Label(card, text="Password", bg=self.colors['card'], font=('Arial', 10)).pack(pady=(10, 5))
        self.password_entry = self.create_styled_entry(card, show="*")
        self.password_entry.pack(pady=5, padx=40, fill=tk.X)

        # Buttons
        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(pady=20)
        
        self.create_styled_button(btn_frame, "Login", self.login, 'success').pack(pady=5)
        self.create_styled_button(btn_frame, "Register", self.register_screen, 'primary').pack(pady=5)

    def register_screen(self):
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        card = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=2)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=500)

        tk.Label(
            card, 
            text="Create Account", 
            font=("Arial", 20, "bold"),
            bg=self.colors['card'],
            fg=self.colors['primary']
        ).pack(pady=20)

        tk.Label(card, text="Username", bg=self.colors['card'], font=('Arial', 10)).pack(pady=(10, 5))
        self.reg_username = self.create_styled_entry(card)
        self.reg_username.pack(pady=5, padx=40, fill=tk.X)

        tk.Label(card, text="Password", bg=self.colors['card'], font=('Arial', 10)).pack(pady=(10, 5))
        self.reg_password = self.create_styled_entry(card, show="*")
        self.reg_password.pack(pady=5, padx=40, fill=tk.X)

        tk.Label(card, text="Email", bg=self.colors['card'], font=('Arial', 10)).pack(pady=(10, 5))
        self.reg_email = self.create_styled_entry(card)
        self.reg_email.pack(pady=5, padx=40, fill=tk.X)

        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(pady=20)
        
        self.create_styled_button(btn_frame, "Submit", self.register, 'success').pack(pady=5)
        self.create_styled_button(btn_frame, "Back to Login", self.login_screen, 'primary').pack(pady=5)

    def register(self):
        uname = self.reg_username.get()
        pwd = self.reg_password.get()
        email = self.reg_email.get()

        if register_user(uname, pwd, email, 'customer'):
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
            self.user_role = get_user_role(user)
            messagebox.showinfo("Welcome", f"Welcome {user[1]}!")
            
            # Check if admin based on credentials
            if uname == "admin" and pwd == "admin123":
                self.user_role = 'admin'
                self.admin_dashboard()
            else:
                self.user_role = 'customer'
                self.customer_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def customer_dashboard(self):
        self.clear_screen()
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header, 
            text=f"Welcome, {self.user[1]}! 👋", 
            font=("Arial", 18, "bold"),
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=20)
        
        # Content area
        content = tk.Frame(main_frame, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        tk.Label(
            content, 
            text="Customer Dashboard", 
            font=("Arial", 16, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        self.create_styled_button(content, "🔍 Search / Filter Products", self.search_products_screen, 'primary', 30).pack(pady=8)
        self.create_styled_button(content, "📋 View All Products", self.view_products, 'primary', 30).pack(pady=8)
        self.create_styled_button(content, "🛒 Shop Now", self.add_to_cart_screen, 'success', 30).pack(pady=8)
        self.create_styled_button(content, "📜 Order History", self.view_order_history, 'primary', 30).pack(pady=8)
        self.create_styled_button(content, "🚪 Logout", self.login_screen, 'danger', 30).pack(pady=8)

    def admin_dashboard(self):
        self.clear_screen()
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg=self.colors['warning'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header, 
            text=f"Admin Panel - {self.user[1]} 👨‍💼", 
            font=("Arial", 18, "bold"),
            bg=self.colors['warning'],
            fg='white'
        ).pack(pady=20)
        
        # Content area
        content = tk.Frame(main_frame, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        tk.Label(
            content, 
            text="Product & Order Management", 
            font=("Arial", 14, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        self.create_styled_button(content, "🔍 Search / Filter Products", self.search_products_screen, 'primary', 30).pack(pady=5)
        self.create_styled_button(content, "➕ Add Product", self.add_product_screen, 'success', 30).pack(pady=5)
        self.create_styled_button(content, "✏️ Update Product", self.update_product_screen, 'primary', 30).pack(pady=5)
        self.create_styled_button(content, "🗑️ Delete Product", self.delete_product_screen, 'danger', 30).pack(pady=5)
        self.create_styled_button(content, "📋 View All Products", self.view_products, 'primary', 30).pack(pady=5)
        self.create_styled_button(content, "📦 View All Orders", self.view_all_orders, 'primary', 30).pack(pady=5)
        self.create_styled_button(content, "📊 Dashboard Summary", self.view_summary, 'primary', 30).pack(pady=5)
        self.create_styled_button(content, "🚪 Logout", self.login_screen, 'danger', 30).pack(pady=10)

    def view_products(self):
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        tk.Label(
            main_frame, 
            text="📋 All Products", 
            font=("Arial", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(pady=20)

        # Product list with scrollbar
        list_frame = tk.Frame(main_frame, bg=self.colors['card'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        product_text = tk.Text(
            list_frame, 
            font=("Courier New", 10),
            yscrollcommand=scrollbar.set,
            bg=self.colors['card'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        product_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=product_text.yview)

        products = view_all_products()
        for p in products:
            product_info = f"ID: {p[0]:3d} | {p[1]:25s} | Category: {p[2]:15s} | ₹{p[3]:8.2f} | Stock: {p[4]:3d}\n"
            product_text.insert(tk.END, product_info)
        
        product_text.config(state=tk.DISABLED)

        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        back_cmd = self.admin_dashboard if self.user_role == 'admin' else self.customer_dashboard
        self.create_styled_button(btn_frame, "🔙 Back", back_cmd, 'primary').pack()

    def add_product_screen(self):
        # Check admin access
        if self.user_role != 'admin':
            messagebox.showerror("Access Denied", "Only admin can add products!")
            return
            
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        card = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=2)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=500)
        
        tk.Label(
            card, 
            text="➕ Add New Product", 
            font=("Arial", 18, "bold"),
            bg=self.colors['card'],
            fg=self.colors['success']
        ).pack(pady=20)

        entries = {}
        for label in ["Name", "Category", "Price", "Stock"]:
            tk.Label(card, text=label, bg=self.colors['card'], font=('Arial', 11)).pack(pady=(10, 5))
            entry = self.create_styled_entry(card)
            entry.pack(pady=5, padx=40, fill=tk.X)
            entries[label.lower()] = entry

        def submit():
            try:
                name = entries["name"].get()
                category = entries["category"].get()
                price = float(entries["price"].get())
                stock = int(entries["stock"].get())
                add_product(name, category, price, stock)
                messagebox.showinfo("Success", "Product added successfully!")
                self.admin_dashboard()
            except:
                messagebox.showerror("Error", "Invalid input. Please check your data.")

        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(pady=20)
        
        self.create_styled_button(btn_frame, "Submit", submit, 'success').pack(pady=5)
        self.create_styled_button(btn_frame, "Cancel", self.admin_dashboard, 'danger').pack(pady=5)

    def update_product_screen(self):
        # Check admin access
        if self.user_role != 'admin':
            messagebox.showerror("Access Denied", "Only admin can update products!")
            return
            
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        card = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=2)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=550)
        
        tk.Label(
            card, 
            text="✏️ Update Product", 
            font=("Arial", 18, "bold"),
            bg=self.colors['card'],
            fg=self.colors['primary']
        ).pack(pady=20)

        entries = {}
        for label in ["Product ID", "New Name", "New Category", "New Price", "New Stock"]:
            tk.Label(card, text=label, bg=self.colors['card'], font=('Arial', 10)).pack(pady=(8, 3))
            entry = self.create_styled_entry(card)
            entry.pack(pady=3, padx=40, fill=tk.X)
            entries[label.lower()] = entry

        def submit():
            try:
                pid = int(entries["product id"].get())
                name = entries["new name"].get()
                category = entries["new category"].get()
                price = float(entries["new price"].get())
                stock = int(entries["new stock"].get())
                update_product(pid, name, category, price, stock)
                messagebox.showinfo("Success", "Product updated successfully!")
                self.admin_dashboard()
            except:
                messagebox.showerror("Error", "Invalid input. Please check your data.")

        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(pady=15)
        
        self.create_styled_button(btn_frame, "Update", submit, 'success').pack(pady=5)
        self.create_styled_button(btn_frame, "Cancel", self.admin_dashboard, 'danger').pack(pady=5)

    def delete_product_screen(self):
        # Check admin access
        if self.user_role != 'admin':
            messagebox.showerror("Access Denied", "Only admin can delete products!")
            return
            
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        card = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=2)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=350)
        
        tk.Label(
            card, 
            text="🗑️ Delete Product", 
            font=("Arial", 18, "bold"),
            bg=self.colors['card'],
            fg=self.colors['danger']
        ).pack(pady=30)
        
        tk.Label(
            card, 
            text="⚠️ Warning: This action cannot be undone!", 
            font=("Arial", 10),
            bg=self.colors['card'],
            fg=self.colors['danger']
        ).pack(pady=10)

        tk.Label(card, text="Product ID", bg=self.colors['card'], font=('Arial', 11)).pack(pady=(20, 5))
        entry = self.create_styled_entry(card)
        entry.pack(pady=5, padx=40, fill=tk.X)

        def submit():
            try:
                pid = int(entry.get())
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete product ID {pid}?")
                if confirm:
                    delete_product(pid)
                    messagebox.showinfo("Deleted", "Product deleted successfully!")
                    self.admin_dashboard()
            except:
                messagebox.showerror("Error", "Invalid Product ID.")

        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(pady=20)
        
        self.create_styled_button(btn_frame, "Delete", submit, 'danger').pack(pady=5)
        self.create_styled_button(btn_frame, "Cancel", self.admin_dashboard, 'primary').pack(pady=5)

    def add_to_cart_screen(self):
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            main_frame, 
            text="🛒 Shop Now - Add to Cart", 
            font=("Arial", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['success']
        ).pack(pady=20)

        # Scrollable product list
        canvas_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        canvas = tk.Canvas(canvas_frame, bg=self.colors['card'])
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        products = view_all_products()
        for p in products:
            frame = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=1)
            frame.pack(pady=5, padx=10, fill=tk.X)

            tk.Label(
                frame, 
                text=f"{p[1]}", 
                font=("Arial", 12, "bold"),
                bg='white',
                fg=self.colors['text']
            ).pack(side=tk.LEFT, padx=10)
            
            tk.Label(
                frame, 
                text=f"₹{p[3]}", 
                font=("Arial", 11),
                bg='white',
                fg=self.colors['success']
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                frame, 
                text=f"Stock: {p[4]}", 
                font=("Arial", 10),
                bg='white',
                fg=self.colors['text_light']
            ).pack(side=tk.LEFT, padx=5)

            qty_var = tk.IntVar(value=1)
            qty_entry = tk.Entry(frame, textvariable=qty_var, width=5, font=("Arial", 10))
            qty_entry.pack(side=tk.LEFT, padx=10)

            add_btn = tk.Button(
                frame, 
                text="Add to Cart",
                command=lambda pid=p[0], qty=qty_var: self.add_to_cart(pid, qty),
                bg=self.colors['success'],
                fg='white',
                font=('Arial', 9, 'bold'),
                relief=tk.FLAT,
                cursor='hand2'
            )
            add_btn.pack(side=tk.LEFT, padx=5, pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        self.create_styled_button(btn_frame, "📋 View Cart", self.view_cart, 'primary', 15).pack(side=tk.LEFT, padx=5)
        self.create_styled_button(btn_frame, "🔙 Back", self.customer_dashboard, 'primary', 15).pack(side=tk.LEFT, padx=5)

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
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            main_frame, 
            text="🛒 Your Shopping Cart", 
            font=("Arial", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(pady=20)

        items = get_cart_items()
        
        content_frame = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=1)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        if not items:
            tk.Label(
                content_frame, 
                text="Your cart is empty 😞", 
                font=("Arial", 14),
                bg=self.colors['card'],
                fg=self.colors['text_light']
            ).pack(pady=50)
        else:
            for item in items:
                item_frame = tk.Frame(content_frame, bg='white', relief=tk.SOLID, borderwidth=1)
                item_frame.pack(pady=5, padx=10, fill=tk.X)
                
                tk.Label(
                    item_frame, 
                    text=f"Product ID: {item[0]} | Quantity: {item[1]}", 
                    font=("Arial", 11),
                    bg='white',
                    fg=self.colors['text']
                ).pack(pady=10, padx=10)

            btn_frame = tk.Frame(content_frame, bg=self.colors['card'])
            btn_frame.pack(pady=20)
            self.create_styled_button(btn_frame, "✅ Checkout", self.checkout, 'success').pack()

        back_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        back_frame.pack(pady=10)
        self.create_styled_button(back_frame, "🔙 Back", self.add_to_cart_screen, 'primary').pack()

    def checkout(self):
        success, msg = place_order(self.user[0])
        if success:
            messagebox.showinfo("Order Placed", msg)
            self.customer_dashboard()
        else:
            messagebox.showerror("Failed", msg)

    def view_order_history(self):
        from models.order_model import view_orders
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            main_frame, 
            text="📜 Your Order History", 
            font=("Arial", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(pady=20)

        orders, items = view_orders(self.user[0])

        content_frame = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=1)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        if not orders:
            tk.Label(
                content_frame, 
                text="You have no orders yet. 🛍️", 
                font=("Arial", 14),
                bg=self.colors['card'],
                fg=self.colors['text_light']
            ).pack(pady=50)
        else:
            canvas = tk.Canvas(content_frame, bg=self.colors['card'])
            scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for o in orders:
                order_card = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=2)
                order_card.pack(pady=10, padx=10, fill=tk.X)
                
                tk.Label(
                    order_card, 
                    text=f"Order ID: {o[0]} | Total: ₹{o[2]:.2f} | Date: {o[3]}",
                    font=("Arial", 11, "bold"),
                    bg='white',
                    fg=self.colors['primary']
                ).pack(pady=5, padx=10, anchor='w')

                for i in items:
                    if i[0] == o[0]:
                        tk.Label(
                            order_card, 
                            text=f"  • Product: {i[1]} | Quantity: {i[2]}",
                            font=("Arial", 10),
                            bg='white',
                            fg=self.colors['text']
                        ).pack(pady=2, padx=20, anchor='w')
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        self.create_styled_button(btn_frame, "🔙 Back", self.customer_dashboard, 'primary').pack()

    def view_all_orders(self):
        # Check admin access
        if self.user_role != 'admin':
            messagebox.showerror("Access Denied", "Only admin can view all orders!")
            return
            
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            main_frame, 
            text="📦 All Customer Orders", 
            font=("Arial", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['warning']
        ).pack(pady=20)

        from db_config import connect_db
        db = connect_db()
        cursor = db.cursor()

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

        content_frame = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=1)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        if not orders:
            tk.Label(
                content_frame, 
                text="No orders found.", 
                font=("Arial", 14),
                bg=self.colors['card'],
                fg=self.colors['text_light']
            ).pack(pady=50)
        else:
            canvas = tk.Canvas(content_frame, bg=self.colors['card'])
            scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for o in orders:
                order_card = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=2)
                order_card.pack(pady=8, padx=10, fill=tk.X)
                
                tk.Label(
                    order_card, 
                    text=f"Order ID: {o[0]} | Customer: {o[1]} | ₹{o[2]:.2f} | {o[3]}",
                    font=("Arial", 11, "bold"),
                    bg='white',
                    fg=self.colors['primary']
                ).pack(pady=5, padx=10, anchor='w')
                
                for i in items:
                    if i[0] == o[0]:
                        tk.Label(
                            order_card, 
                            text=f"  • {i[1]} x {i[2]}",
                            font=("Arial", 10),
                            bg='white',
                            fg=self.colors['text']
                        ).pack(pady=2, padx=20, anchor='w')
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        self.create_styled_button(btn_frame, "🔙 Back", self.admin_dashboard, 'primary').pack()

    def view_summary(self):
        # Check admin access
        if self.user_role != 'admin':
            messagebox.showerror("Access Denied", "Only admin can view dashboard summary!")
            return
            
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            main_frame, 
            text="📊 Dashboard Summary", 
            font=("Arial", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['warning']
        ).pack(pady=20)

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

        # Stats cards
        stats_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        stats_frame.pack(pady=20)
        
        # Users card
        user_card = tk.Frame(stats_frame, bg=self.colors['primary'], width=200, height=100)
        user_card.pack(side=tk.LEFT, padx=10)
        tk.Label(user_card, text=f"👥 {user_count}", font=("Arial", 20, "bold"), bg=self.colors['primary'], fg='white').pack(pady=10)
        tk.Label(user_card, text="Total Users", font=("Arial", 11), bg=self.colors['primary'], fg='white').pack()
        
        # Products card
        prod_card = tk.Frame(stats_frame, bg=self.colors['success'], width=200, height=100)
        prod_card.pack(side=tk.LEFT, padx=10)
        tk.Label(prod_card, text=f"📦 {product_count}", font=("Arial", 20, "bold"), bg=self.colors['success'], fg='white').pack(pady=10)
        tk.Label(prod_card, text="Total Products", font=("Arial", 11), bg=self.colors['success'], fg='white').pack()
        
        # Orders card
        order_card = tk.Frame(stats_frame, bg=self.colors['warning'], width=200, height=100)
        order_card.pack(side=tk.LEFT, padx=10)
        tk.Label(order_card, text=f"🧾 {order_count}", font=("Arial", 20, "bold"), bg=self.colors['warning'], fg='white').pack(pady=10)
        tk.Label(order_card, text="Total Orders", font=("Arial", 11), bg=self.colors['warning'], fg='white').pack()

        # Low stock section
        low_stock_frame = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=2)
        low_stock_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        if low_stock_items:
            tk.Label(
                low_stock_frame, 
                text="⚠️ Low Stock Items (<5)", 
                font=("Arial", 14, "bold"),
                bg=self.colors['card'],
                fg=self.colors['danger']
            ).pack(pady=10)
            
            for item in low_stock_items:
                tk.Label(
                    low_stock_frame, 
                    text=f"• {item[0]} - Only {item[1]} left",
                    font=("Arial", 11),
                    bg=self.colors['card'],
                    fg=self.colors['text']
                ).pack(pady=3)
        else:
            tk.Label(
                low_stock_frame, 
                text="✅ All items are sufficiently stocked.",
                font=("Arial", 12),
                bg=self.colors['card'],
                fg=self.colors['success']
            ).pack(pady=30)

        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        self.create_styled_button(btn_frame, "🔙 Back", self.admin_dashboard, 'primary').pack()

    def search_products_screen(self):
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            main_frame, 
            text="🔍 Search / Filter Products", 
            font=("Arial", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(pady=20)

        search_frame = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=1)
        search_frame.pack(padx=40, pady=10, fill=tk.X)
        
        tk.Label(search_frame, text="Search by Name:", bg=self.colors['card'], font=('Arial', 11)).pack(pady=(10, 5))
        name_entry = self.create_styled_entry(search_frame)
        name_entry.pack(pady=5, padx=20, fill=tk.X)

        tk.Label(search_frame, text="Filter by Category:", bg=self.colors['card'], font=('Arial', 11)).pack(pady=(10, 5))
        category_var = tk.StringVar()
        category_dropdown = tk.OptionMenu(search_frame, category_var, "All")
        category_dropdown.config(font=('Arial', 10), bg='white')
        category_dropdown.pack(pady=5, padx=20, fill=tk.X)

        result_frame = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, borderwidth=1)
        result_frame.pack(padx=40, pady=10, fill=tk.BOTH, expand=True)
        
        result_box = tk.Text(
            result_frame, 
            width=70, 
            height=15,
            font=("Courier New", 10),
            bg='white',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        result_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

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
                result_box.insert(tk.END, f"{'ID':<5} {'Name':<25} {'Category':<15} {'Price':<10} {'Stock':<5}\n")
                result_box.insert(tk.END, "-" * 70 + "\n")
                for p in results:
                    result_box.insert(tk.END,
                                      f"{p[0]:<5} {p[1]:<25} {p[2]:<15} ₹{p[3]:<9.2f} {p[4]:<5}\n")

        btn_container = tk.Frame(search_frame, bg=self.colors['card'])
        btn_container.pack(pady=15)
        
        self.create_styled_button(btn_container, "🔍 Search", search, 'success', 15).pack()

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

        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        back_cmd = self.admin_dashboard if self.user_role == 'admin' else self.customer_dashboard
        self.create_styled_button(btn_frame, "🔙 Back", back_cmd, 'primary').pack()

