# 🛒 Modern Grocery Store - Complete E-Commerce Application

A feature-rich desktop e-commerce application built with Python and Tkinter, designed for real-world grocery store operations. Inspired by platforms like Amazon and Daraz, this app provides separate interfaces for customers and staff with comprehensive inventory management, order tracking, and notifications.

---

## ✨ Key Features

### 👥 For Customers
- **User Registration & Login** - Secure account creation with bcrypt password hashing
- **Category-Based Shopping** - Browse products organized by categories with icons
- **Product Search** - Find products quickly by name or description
- **Shopping Cart** - Add items, update quantities, and manage your cart
- **Secure Checkout** - Place orders with delivery information and payment options
- **Order Tracking** - View complete order history with status updates
- **Real-Time Notifications** - Get notified about order confirmations, shipments, and deliveries
- **Profile Management** - Update personal information and addresses

### 👨‍💼 For Staff/Admin
- **Separate Staff Login** - Dedicated authentication for admin and staff
- **Product Management** - Add products with images, descriptions, pricing, and categories
- **Image Upload** - Attach product photos for better customer experience
- **Inventory Tracking** - Monitor stock levels, batch numbers, and expiry dates
- **Batch Management** - Track inventory with supplier info, purchase price, and expiry
- **Low Stock Alerts** - Automatic alerts when products fall below minimum levels
- **Expiry Management** - Track products nearing expiry date
- **Order Management** - View all customer orders and update order statuses
- **Dashboard Analytics** - Real-time statistics on inventory value, stock levels, and alerts

---

## 🗂️ Database Architecture

### Complete Database Schema
The application uses **MySQL** with the following tables:

#### Core Tables
1. **users** - Customer accounts with full profile information
2. **staff** - Admin/staff accounts with role-based access
3. **categories** - Product categories with icons
4. **products** - Customer-facing products with images and pricing
5. **inventory** - Stock management with batches, expiry dates, and suppliers
6. **shopping_cart** - Temporary cart items for logged-in users
7. **orders** - Customer orders with payment and delivery info
8. **order_items** - Items within each order (snapshot at purchase time)
9. **notifications** - User notifications for order updates
10. **product_reviews** - Customer product reviews (future feature)
11. **activity_log** - Staff action tracking for audit purposes

#### Database Views
- **low_stock_products** - Products below minimum stock level
- **product_sales_summary** - Sales analytics by product
- **user_order_summary** - Customer purchase history summary

#### Stored Procedures
- **add_to_cart** - Add items to cart with stock validation
- **place_order** - Complete order placement with inventory updates

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install mysql-connector-python bcrypt pillow
```

### Step 2: Configure Database Connection
Edit `db_config.py` with your MySQL credentials:
```python
host="localhost"
user="root"
password="YOUR_MYSQL_PASSWORD"  # Update this!
database="grocery_app_db"
```

### Step 3: Create Database
Run the setup script to create the database and initial data:
```bash
python setup_database.py
```

This will:
- Create `grocery_app_db` database
- Set up all tables with relationships
- Create default categories
- Insert sample products
- Create admin user (username: admin, password: admin123)
- Create product_images folder

### Step 4: Run the Application
```bash
python main.py
```

---

## 🔐 Default Credentials

### Admin Login
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@groceryapp.com`

### Customer
- Register a new account from the login screen

---

## 📁 Project Structure

```
Grocery_App/
├── main.py                     # Application entry point
├── setup_database.py           # Database setup script
├── database_schema.sql         # Complete SQL schema
├── db_config.py               # Database configuration
├── README.md                  # This file
│
├── models/                    # Data models (Business logic)
│   ├── user_model.py         # User & staff authentication
│   ├── product_model.py      # Product management
│   ├── order_model.py        # Shopping cart & orders
│   └── inventory_model.py    # Inventory & batch tracking
│
├── gui/                       # User interface
│   ├── modern_app.py         # Main modern UI (NEW)
│   └── app_window.py         # Legacy UI (backup)
│
├── utils/                     # Utility functions
│   └── image_helper.py       # Image upload & management
│
└── product_images/            # Uploaded product images
```

---

## 🎨 User Interface Highlights

### Modern Design
- **Clean, card-based layout** inspired by modern e-commerce platforms
- **Color-coded sections** for easy navigation
- **Responsive buttons** with hover effects
- **Scrollable content** for better data presentation
- **Image support** for products with fallback placeholders

### Customer Experience
1. **Login/Register** - Simple authentication with user type selection
2. **Dashboard** - Quick access to shopping, cart, orders, and profile
3. **Shop** - Category sidebar with grid-based product display
4. **Product Cards** - Images, prices, discounts, and stock info
5. **Cart** - Update quantities, remove items, see totals
6. **Checkout** - Delivery form with payment method selection
7. **Orders** - Timeline view of order history with status badges
8. **Notifications** - Alert center for order updates

### Admin Experience
1. **Dashboard** - Key metrics: inventory value, stock levels, expiry alerts
2. **Add Product** - Form with image upload, categories, and pricing
3. **Manage Products** - Edit, delete, or disable products
4. **Inventory** - Batch tracking with expiry dates and supplier info
5. **Orders** - View all customer orders, update statuses

---

## 📊 Key Workflows

### Customer Shopping Flow
```
Login/Register → Browse Categories → Add to Cart → Checkout → Place Order → Get Notification
```

### Admin Product Management Flow
```
Login as Staff → Add Product (with image) → Set pricing & stock → Product goes live → Monitor inventory
```

### Inventory Management Flow
```
Receive Stock → Add Inventory Batch → Set expiry date → Track usage → Get alerts for low/expiring stock
```

---

## 🔧 Advanced Features

### Image Management
- Upload product images in any common format (PNG, JPG, JPEG, GIF)
- Automatic resizing and optimization
- Safe filename generation
- Fallback to placeholder if image missing

### Notification System
- Automatic notifications for:
  - Order placed
  - Order confirmed
  - Order shipped
  - Order delivered
- Unread notification counter
- Mark as read functionality

### Inventory Tracking
- Batch number assignment
- Purchase price vs selling price tracking
- Supplier information
- Received and expiry dates
- Quantity remaining alerts

### Order Management
- Order number generation (ORD-YYYYMMDD-XXXX)
- Multiple status levels: pending, confirmed, processing, shipped, delivered
- Payment method tracking
- Delivery address storage
- Order history with item snapshots

---

## 🛡️ Security Features

- **Password Hashing** - bcrypt with salt
- **SQL Injection Protection** - Parameterized queries
- **Role-Based Access** - Separate customer and staff tables
- **Session Management** - User context throughout the app
- **Input Validation** - All user inputs validated

---

## 📝 Usage Guide

### For Customers

1. **Register an Account**
   - Click "Register as Customer"
   - Fill in username, password, email (required)
   - Add full name, phone, address (optional but recommended for checkout)

2. **Browse & Shop**
   - Select "Shop Now" from dashboard
   - Choose category from sidebar
   - View product details, prices, and stock
   - Add items to cart with desired quantity

3. **Checkout**
   - Go to "My Cart"
   - Review items and quantities
   - Click "Proceed to Checkout"
   - Enter delivery address and phone
   - Select payment method
   - Place order

4. **Track Orders**
   - View "My Orders"
   - Check order status
   - See delivery updates via notifications

### For Admin/Staff

1. **Login**
   - Select "Staff/Admin" option
   - Use admin credentials

2. **Add Products**
   - Go to "Add Product"
   - Upload product image
   - Fill in name, category, description
   - Set price and unit type
   - Enter initial stock quantity
   - Set minimum stock level for alerts

3. **Manage Inventory**
   - View inventory batches
   - Add new stock with supplier info
   - Set expiry dates
   - Monitor low stock and expiring items

4. **Process Orders**
   - View all customer orders
   - Update order statuses
   - Customers get automatic notifications

---

## 🐛 Troubleshooting

### Database Connection Error
- Verify MySQL server is running
- Check credentials in `db_config.py`
- Ensure database `grocery_app_db` exists

### Image Not Displaying
- Check `product_images/` folder exists
- Verify PIL/Pillow is installed: `pip install pillow`
- Ensure image path is correct in database

### Import Errors
- Install all dependencies: `pip install mysql-connector-python bcrypt pillow`
- Check Python version: `python --version` (should be 3.7+)

---

## 🚧 Future Enhancements

- [ ] Product reviews and ratings
- [ ] Advanced search with filters
- [ ] Wishlist functionality
- [ ] Discount/coupon system
- [ ] Sales reports and analytics
- [ ] Email notifications
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Payment gateway integration
- [ ] Barcode scanner integration

---

## 📄 License

This project is created for educational purposes.

---

## 👨‍💻 Technical Stack

- **Frontend:** Tkinter, PIL (Pillow)
- **Backend:** Python 3.x
- **Database:** MySQL 8.0
- **Authentication:** bcrypt
- **Image Processing:** Pillow (PIL Fork)

---

## 🆘 Support

For issues or questions:
1. Check this README carefully
2. Verify database setup completed successfully
3. Ensure all dependencies are installed
4. Check MySQL service is running
5. Review error messages in terminal

---

**Develop By PaveshDev**

*Transform your grocery business with digital excellence!*

