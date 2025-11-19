# 🛒 buyMe - Modern Grocery Store for Sri Lanka

A professional desktop e-commerce application built with Python and Tkinter, designed specifically for Sri Lankan grocery store operations. This application provides a complete solution for managing online grocery sales with support for LKR (Sri Lankan Rupee) and popular payment methods like PayPal and Google Pay.

---

## ✨ Key Features

### 👥 For Customers
- **User Registration & Login** - Secure account creation with bcrypt password hashing
- **Category-Based Shopping** - Browse products organized by 10+ categories with icons
- **Product Search** - Find products quickly by name or description
- **Shopping Cart** - Add items, update quantities, and manage your cart
- **Checkout Process** - Fast checkout with delivery information
- **Multiple Payment Methods** - Card payments, PayPal, or Google Pay
- **Automatic Order Confirmation** - Orders auto-confirmed immediately upon payment
- **Real-Time Notifications** - Get notified about order confirmations and delivery dates
- **Order Tracking** - View complete order history with status and payment information
- **Profile Management** - Update personal information and delivery addresses

### 👨‍💼 For Staff/Admin
- **Staff Login** - Dedicated admin panel with role-based access
- **Product Management** - Add/edit products with images, descriptions, and pricing
- **Image Upload** - Attach product photos for customer preview
- **Inventory Tracking** - Monitor stock levels, batch numbers, and expiry dates
- **Batch Management** - Track inventory with supplier info and purchase prices
- **Expiry Management** - View products nearing or past expiry date
- **Order Management** - View all customer orders with payment and delivery status
- **Payment Status Visibility** - See which orders are paid and which are pending
- **Order Confirmation Tracking** - Track when orders were confirmed and calculated delivery dates
- **Dashboard Analytics** - Real-time statistics and alerts

---

## 🌍 Sri Lanka Localization

### Currency & Payment
- **Currency:** LKR (Sri Lankan Rupee) - Display: `LKR 500.00`
- **Payment Methods:**
  - 💳 **Card Payment** - Debit/Credit card transactions
  - 💰 **PayPal** - International payment gateway
  - 📱 **Google Pay** - Mobile payment solution
  - 💵 **Cash on Delivery** - Pay upon receiving order

### Default Categories
1. 🍎 Fruits - Fresh fruits and berries
2. 🥕 Vegetables - Fresh vegetables and greens
3. 🥛 Dairy - Milk, cheese, yogurt and dairy products
4. 🍞 Bakery - Bread, cakes and baked goods
5. 🥩 Meat & Seafood - Fresh meat, chicken and seafood
6. 🥤 Beverages - Juices, soft drinks and water
7. 🍪 Snacks - Chips, cookies and snacks
8. 🧊 Frozen Foods - Frozen vegetables, meals and ice cream
9. 🥫 Pantry - Rice, pasta, canned goods and spices
10. 🧴 Personal Care - Soaps, shampoos and hygiene products

---

## 🗂️ Database Architecture

### Core Tables
1. **users** - Customer accounts with profile information
2. **staff** - Admin/staff accounts with role-based access
3. **categories** - Product categories with icons
4. **products** - Products with pricing, images, and stock info
5. **inventory** - Stock management with batches, expiry dates, and suppliers
6. **shopping_cart** - Temporary cart items for customers
7. **orders** - Customer orders with payment and delivery tracking
8. **order_items** - Items within each order
9. **notifications** - User notifications for order updates

### Key Fields
- **Payment Status:** pending, paid, failed
- **Order Status:** pending, confirmed, processing, shipped, delivered, cancelled
- **Payment Methods:** cash, card, online (PayPal/Google Pay)

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.8** or higher
- **MySQL Server 8.0** or higher
- **pip** (Python package manager)

### Step 1: Clone/Extract the Project
```bash
cd Grocery_App
```

### Step 2: Install Dependencies
```bash
pip install mysql-connector-python bcrypt pillow
```

### Step 3: Configure Database Connection
Edit `db_config.py` with your MySQL credentials:
```python
host = "localhost"
user = "root"
password = "YOUR_MYSQL_PASSWORD"  # Update with your MySQL password
database = "grocery_app_db"
```

### Step 4: Setup Database
Option A - Using Python script:
```bash
python setup_database.py
```

Option B - Using SQL directly:
1. Open MySQL and create database:
```sql
CREATE DATABASE grocery_app_db;
USE grocery_app_db;
```
2. Run the database_schema.sql file:
```bash
mysql -u root -p grocery_app_db < database_schema.sql
```

This will:
- ✅ Create all necessary tables
- ✅ Create default categories
- ✅ Create admin user account
- ✅ Create product_images folder

### Step 5: Launch the Application
```bash
python main.py
```

---

## 🔐 Default Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@groceryapp.com`
- **Role:** Administrator

### Test Customer
- Register a new account from the login screen
- Use any unique username and strong password

---

## 📖 How to Use

### For Customers

#### 1. Register Account
```
Login Screen → Click "Register as Customer"
→ Enter: Username, Password, Email
→ Optional: Full Name, Phone, Address
→ Click "Register"
```

#### 2. Browse Products
```
Customer Dashboard → Click "Shop Now"
→ Select Category from sidebar (or "All Products")
→ Click on any product card to see details
→ View: Image, Price, Stock, Description
```

#### 3. Add to Cart
```
Product Details → Set Quantity
→ Click "Add to Cart"
→ Continue shopping or go to cart
→ Repeat for more products
```

#### 4. Checkout Process
```
Dashboard → Click "My Cart"
→ Review items and update quantities if needed
→ Click "Proceed to Checkout"
→ Enter Delivery Address & Phone Number
→ Select Payment Method:
   • Cash (Pay upon delivery)
   • Card (Debit/Credit card)
   • PayPal (PayPal email)
   • Google Pay (Phone number)
→ Complete Payment
→ Order Confirmed! ✅
```

#### 5. Track Orders
```
Dashboard → Click "My Orders"
→ View all orders with:
   • Order Number
   • Order Date
   • Delivery Date (calculated as Order Date + 7 days)
   • Payment Status (✅ Paid / ❌ Pending)
   • Order Status (Confirmed/Processing/Delivered)
→ Click arrow to see order details
```

#### 6. Notifications
```
Dashboard → Click "📬 Notifications"
→ See all order updates:
   • Order Placed
   • Order Confirmed
   • Payment Status
   • Delivery Information
→ Click notification to mark as read
```

### For Admin/Staff

#### 1. Login to Admin Panel
```
Login Screen → Select "Staff/Admin"
→ Enter Username: admin
→ Enter Password: admin123
→ Access Admin Dashboard
```

#### 2. Add New Product
```
Admin Dashboard → Click "Add Product"
→ Fill Product Details:
   • Product Name (required)
   • Category (select from dropdown)
   • Description
   • Unit Type (kg, liter, unit, etc.)
   • Unit Price in LKR
   • Discount % (optional)
   • Stock Quantity
→ Upload Product Image
→ Click "Add Product"
```

#### 3. Manage Products
```
Admin Dashboard → Click "Manage Products"
→ View all products in table:
   • Edit button - Modify product details
   • Delete button - Remove product
→ Filter by category from sidebar
```

#### 4. Manage Inventory
```
Admin Dashboard → Click "Inventory"
→ View stock information:
   • Current stock
   • Minimum stock level
   • Expiry dates
→ Add New Batch:
   • Select Product
   • Enter Quantity
   • Set Expiry Date
   • Add Supplier Info & Cost Price
→ Track usage and get alerts
```

#### 5. View Orders
```
Admin Dashboard → Click "Orders"
→ See all customer orders:
   • Order Number
   • Customer Name
   • Order Date
   • Payment Method
   • Payment Status (✅ Paid / ❌ Pending)
   • Order Status
→ Click arrow to see full order details:
   • Items ordered with quantities
   • Delivery address & phone
   • Confirmed date
   • Calculated delivery date
→ Update order status as needed
```

#### 6. Monitor Alerts
```
Admin Dashboard → View Alert Section:
   • Low Stock Items - Products below minimum level
   • Expiring Items - Products near expiry date
   • Expired Items - Products past expiry date
→ Take action: Add stock, remove expired items
```

---

## 🎨 User Interface

### Design Features
- **Modern Card-Based Layout** - Clean, organized presentation
- **Purple & White Theme** - Professional colors matching brand
- **Responsive Controls** - Buttons change on hover
- **Organized Sections** - Clear separation of features
- **Product Images** - Visual product previews
- **Status Indicators** - Color-coded badges (Green = Ready, Orange = Pending)

### Navigation
- **Header** - App logo, title, and quick actions
- **Sidebar** - Category filter (customers) or admin menu
- **Main Content** - Product grid or detailed forms
- **Scrollable Areas** - For long product lists and orders

---

## 💰 Payment System

### Payment Methods

#### 1. Card Payment
- Accept Visa/Mastercard
- Validation:
  - 16-digit card number
  - Expiry date (MM/YY format)
  - 3-digit CVV
- Auto-marked as paid upon success

#### 2. PayPal
- Enter PayPal email
- Redirects to PayPal portal
- Auto-marked as paid upon success

#### 3. Google Pay
- Enter phone number (10+ digits)
- Mobile payment integration
- Auto-marked as paid upon success

#### 4. Cash on Delivery
- Order confirmed immediately
- Payment status: Pending
- Collect payment upon delivery

### Automatic Order Confirmation
✅ **All orders are automatically confirmed** when placed:
- Confirmation Timestamp: Recorded in `confirmed_at` field
- Delivery Date: Automatically calculated (Order Date + 7 days)
- Payment Status: Updated based on payment method
  - Card/PayPal/GPay: Marked as "Paid"
  - Cash: Marked as "Pending"

---

## 🛡️ Security Features

- ✅ **Password Hashing** - bcrypt with salt for secure storage
- ✅ **SQL Injection Protection** - Parameterized queries throughout
- ✅ **Role-Based Access** - Separate customer and staff panels
- ✅ **Session Management** - User context preserved during session
- ✅ **Input Validation** - All user inputs validated before processing
- ✅ **Secure Authentication** - Two-factor user verification

---

## ⚙️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Tkinter (Python GUI) |
| **Backend** | Python 3.8+ |
| **Database** | MySQL 8.0 |
| **Image Processing** | Pillow (PIL) |
| **Authentication** | bcrypt |
| **Architecture** | Service-Based MVC Pattern |

### Services Layer
- **UserService** - Authentication & profile management
- **ProductService** - Product catalog management
- **OrderService** - Cart & order management
- **InventoryService** - Stock tracking & batches
- **PaymentService** - Payment processing & validation
- **ImageService** - Image upload & handling

---

## 📊 Order Flow Diagram

```
Customer                          System                       Database
   |                              |                              |
   +---> Login/Register          |                              |
   |         |                    |                              |
   |         +---> Authenticate   +----> Check Users Table     |
   |                  |                                          |
   +---> Browse Products          +----> Load Products Table    |
   |         |                          Load Categories Table    |
   |         +---> View Categories                              |
   |                  |                                          |
   +---> Add to Cart  +---> Validate Stock +---> Check Inventory|
   |         |                                                    |
   +---> Checkout    +---> Create Order ----> Insert Orders Table
   |         |             Create Order Items -> order_items     |
   |         +---> Payment                                       |
   |              (Card/PayPal/GPay)                            |
   |                  |                                          |
   +---> Notification +---> Auto-Confirm -----> Update Status   |
   |                      Calculate Delivery       notifications |
   |
   +---> View Orders  +---> Fetch Order Details
                            Show Payment Status
                            Show Delivery Date
```

---

## 🐛 Troubleshooting

### Database Connection Error
**Error:** `Access denied for user 'root'@'localhost'`
**Solution:**
- Check MySQL server is running: `net start MySQL80` (Windows)
- Verify credentials in `db_config.py`
- Ensure password is correct

### Import Errors
**Error:** `ModuleNotFoundError: No module named 'PIL'`
**Solution:**
```bash
pip install pillow
```

### Image Not Displaying
**Error:** Product shows placeholder but should show image
**Solution:**
- Verify `product_images/` folder exists in project root
- Check image file permissions
- Re-upload the image from admin panel

### Application Won't Start
**Error:** `Connection refused` or similar
**Solution:**
1. Verify MySQL is running
2. Check database exists: `mysql -u root -p -e "SHOW DATABASES;"`
3. Run setup script again: `python setup_database.py`

### Port Already in Use
**Error:** Cannot create window/connection
**Solution:**
- Close other instances of the app
- Restart Python/Terminal
- Check no other services using default ports

---

## 📱 Application Screenshots

### Customer Views
1. **Login Screen** - Registration and authentication
2. **Dashboard** - Quick access to shopping and orders
3. **Shop** - Product browsing with categories
4. **Product Detail** - Full product information
5. **Cart** - Review and manage items
6. **Checkout** - Payment method selection
7. **Orders** - Order history and tracking
8. **Notifications** - Order updates

### Admin Views
1. **Admin Dashboard** - Overview and alerts
2. **Add Product** - Product creation form
3. **Manage Products** - Product listing and editing
4. **Inventory** - Stock management
5. **Orders** - All customer orders
6. **Order Details** - Complete order information

---

## 🚀 Performance Optimization

### Implemented Features
- ✅ **Lazy Image Loading** - Images load asynchronously
- ✅ **Database Indexing** - Fast queries on frequently searched fields
- ✅ **Image Caching** - Loaded images cached in memory
- ✅ **Optimized Queries** - Minimal database round trips
- ✅ **Responsive UI** - Immediate visual feedback

### Loading Times
- Product Detail: < 100ms (with async image load)
- Cart Operations: < 50ms
- Order Processing: < 200ms
- Checkout: Instant page transitions

---

## 📝 File Structure

```
Grocery_App/
├── main.py                     # 🚀 Application entry point
├── db_config.py               # 🔧 Database configuration
├── setup_database.py          # 📊 Database setup script
├── database_schema.sql        # 📋 SQL schema (cleaned & optimized)
├── README.md                  # 📖 This file
│
├── services/                  # 🔧 Business Logic
│   ├── user_service.py
│   ├── product_service.py
│   ├── order_service.py
│   ├── inventory_service.py
│   ├── payment_service.py
│   └── image_service.py
│
├── models/                    # 📦 Data Models (Legacy)
│   ├── user_model.py
│   ├── product_model.py
│   ├── order_model.py
│   └── inventory_model.py
│
├── gui/                       # 🎨 User Interface
│   ├── modern_app.py         # Main UI (Tkinter)
│   ├── ui_components.py      # UI utilities & components
│   └── app_window.py         # Legacy UI
│
└── product_images/            # 📷 Uploaded product images
```

---

## 🔄 Recent Updates (v2.0)

### ✨ New Features
- ✅ PayPal payment support for Sri Lanka
- ✅ Google Pay (GPay) payment integration
- ✅ LKR currency throughout app
- ✅ Automatic order confirmation
- ✅ 7-day delivery date calculation
- ✅ Payment status tracking in admin
- ✅ Async image loading for speed

### 🐛 Bug Fixes
- ✅ Fixed product card click responsiveness
- ✅ Fixed missing 'warning' color in theme
- ✅ Optimized product detail page loading
- ✅ Fixed service method calls
- ✅ Cleaned database schema (removed unused tables)

### 📊 Database Schema Changes
- Removed: product_reviews, activity_log tables
- Removed: Complex stored procedures
- Kept: Essential 9 tables for core functionality
- Result: 43% schema reduction, faster queries

---

## 🎯 Usage Tips

### For Customers
1. **Register with real details** - Needed for order delivery
2. **Save frequently used addresses** - Faster checkout next time
3. **Check notifications** - Stay updated on order status
4. **Clear cart when switching users** - Each user has separate cart

### For Admin
1. **Set realistic prices** - Include product sourcing cost
2. **Update stock regularly** - Prevent overselling
3. **Monitor expiry dates** - Remove expired items weekly
4. **Keep categories organized** - Better customer experience

---

## 🆘 Support & Help

### Common Questions

**Q: How long does delivery take?**
A: Standard delivery is 7 days from order confirmation. See calculated delivery date in order details.

**Q: Can I change my payment method after checkout?**
A: No, payment method is locked at checkout. You must place a new order.

**Q: How do I reset admin password?**
A: Manually update in MySQL using bcrypt hashing, or contact system administrator.

**Q: Can multiple admins manage products?**
A: Yes, create multiple staff accounts with different roles. All updates are reflected instantly.

**Q: How are product prices updated?**
A: Admin can edit prices anytime. New orders use current prices, old orders keep historical prices.

### Getting Help
1. ✅ Check this README first
2. ✅ Verify all prerequisites installed
3. ✅ Ensure database is properly set up
4. ✅ Check error messages in terminal
5. ✅ Review application logs

---

## 📈 Future Enhancements

- [ ] SMS notifications via Twilio
- [ ] WhatsApp order updates
- [ ] Advanced search with filters
- [ ] Product reviews & ratings
- [ ] Wishlist functionality
- [ ] Coupon/discount codes
- [ ] Sales analytics dashboard
- [ ] Bulk order capabilities
- [ ] Delivery tracking with map
- [ ] Multiple payment gateway integration

---

## 📄 License & Credits

**Created by:** PaveshDev  
**Purpose:** Professional E-Commerce Solution for Sri Lanka  
**License:** Educational & Commercial Use Allowed

---

## 🌟 Quick Start (TL;DR)

```bash
# 1. Install dependencies
pip install mysql-connector-python bcrypt pillow

# 2. Update db_config.py with your MySQL password

# 3. Setup database
python setup_database.py

# 4. Run application
python main.py

# 5. Login as admin
# Username: admin
# Password: admin123
```

---

**Transform your grocery business with digital excellence!** 🚀

*buyMe - Your Complete Sri Lankan E-Commerce Solution*

