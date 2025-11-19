-- ====================================================================
-- Grocery App Database Schema - Sri Lankan E-Commerce System
-- Database: grocery_app_db
-- Currency: LKR (Sri Lankan Rupee)
-- Cleaned & Optimized for buyMe Project
-- ====================================================================

-- Drop database if exists and create fresh
DROP DATABASE IF EXISTS grocery_app_db;
CREATE DATABASE grocery_app_db;
USE grocery_app_db;

-- ====================================================================
-- 1. USERS TABLE - Customer accounts
-- ====================================================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- bcrypt hashed
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- ====================================================================
-- 2. STAFF TABLE - Admin/Staff accounts
-- ====================================================================
CREATE TABLE staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- bcrypt hashed
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role ENUM('admin', 'manager', 'staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_role (role)
);

-- ====================================================================
-- 3. CATEGORIES TABLE - Product categories
-- ====================================================================
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),  -- emoji or icon name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (category_name)
);

-- ====================================================================
-- 4. PRODUCTS TABLE - Items available for sale (customer-facing)
-- ====================================================================
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category_id INT NOT NULL,
    description TEXT,
    image_path VARCHAR(500),  -- Path to product image
    unit_price DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(20) DEFAULT 'unit',  -- kg, liter, unit, etc.
    stock_quantity INT DEFAULT 0,
    min_stock_level INT DEFAULT 5,  -- Alert threshold
    is_available BOOLEAN DEFAULT TRUE,
    discount_percent DECIMAL(5, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE,
    INDEX idx_category (category_id),
    INDEX idx_available (is_available),
    INDEX idx_name (name)
);

-- ====================================================================
-- 5. INVENTORY TABLE - Stock management (admin-facing)
-- ====================================================================
CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    batch_number VARCHAR(50),
    quantity_received INT NOT NULL,
    quantity_remaining INT NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,  -- Cost price
    supplier_name VARCHAR(200),
    received_date DATE NOT NULL,
    expiry_date DATE,
    added_by INT NOT NULL,  -- staff_id
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (added_by) REFERENCES staff(staff_id),
    INDEX idx_product (product_id),
    INDEX idx_expiry (expiry_date),
    INDEX idx_batch (batch_number)
);

-- ====================================================================
-- 6. SHOPPING_CART TABLE - Temporary cart items
-- ====================================================================
CREATE TABLE shopping_cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_product (user_id, product_id),
    INDEX idx_user (user_id)
);

-- ====================================================================
-- 7. ORDERS TABLE - Customer orders
-- ====================================================================
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_number VARCHAR(50) UNIQUE NOT NULL,  -- ORD-20250101-001
    total_amount DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
    final_amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('cash', 'card', 'online', 'wallet') DEFAULT 'cash',
    payment_status ENUM('pending', 'paid', 'failed') DEFAULT 'pending',
    order_status ENUM('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    delivery_address TEXT NOT NULL,
    delivery_phone VARCHAR(20),
    notes TEXT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user (user_id),
    INDEX idx_order_number (order_number),
    INDEX idx_status (order_status),
    INDEX idx_date (order_date)
);

-- ====================================================================
-- 8. ORDER_ITEMS TABLE - Items in each order
-- ====================================================================
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX idx_order (order_id),
    INDEX idx_product (product_id)
);

-- ====================================================================
-- 9. NOTIFICATIONS TABLE - Order and payment notifications
-- ====================================================================
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('order_placed', 'order_confirmed', 'order_shipped', 'order_delivered', 'payment') NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    order_id INT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_read (is_read)
);

-- ====================================================================
-- INSERT DEFAULT DATA
-- ====================================================================

-- Default admin staff (password: admin123)
INSERT INTO staff (username, password, email, full_name, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYsL0MCWm8u', 'admin@groceryapp.com', 'System Administrator', 'admin');

-- Default categories for Sri Lanka
INSERT INTO categories (category_name, description, icon) VALUES
('Fruits', 'Fresh fruits and berries', '🍎'),
('Vegetables', 'Fresh vegetables and greens', '🥕'),
('Dairy', 'Milk, cheese, yogurt and dairy products', '🥛'),
('Bakery', 'Bread, cakes and baked goods', '🍞'),
('Meat & Seafood', 'Fresh meat, chicken and seafood', '🥩'),
('Beverages', 'Juices, soft drinks and water', '🥤'),
('Snacks', 'Chips, cookies and snacks', '🍪'),
('Frozen Foods', 'Frozen vegetables, meals and ice cream', '🧊'),
('Pantry', 'Rice, pasta, canned goods and spices', '🥫'),
('Personal Care', 'Soaps, shampoos and hygiene products', '🧴');


-- ====================================================================
-- END OF SCHEMA
-- ====================================================================

SELECT 'Database grocery_app_db created successfully!' as Status;
