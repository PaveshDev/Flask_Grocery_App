-- ====================================================================
-- Grocery App Database Schema - Complete E-Commerce System
-- Database: grocery_app_db
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
    product_name VARCHAR(200) NOT NULL,  -- Snapshot at order time
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,  -- Price at order time
    discount_percent DECIMAL(5, 2) DEFAULT 0.00,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX idx_order (order_id),
    INDEX idx_product (product_id)
);

-- ====================================================================
-- 9. NOTIFICATIONS TABLE - User notifications
-- ====================================================================
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('order_placed', 'order_confirmed', 'order_shipped', 'order_delivered', 'payment', 'promotion') NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    order_id INT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_read (is_read),
    INDEX idx_created (created_at)
);

-- ====================================================================
-- 10. PRODUCT_REVIEWS TABLE - Customer reviews
-- ====================================================================
CREATE TABLE product_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_product (product_id),
    INDEX idx_user (user_id),
    INDEX idx_rating (rating)
);

-- ====================================================================
-- 11. ACTIVITY_LOG TABLE - Track admin actions
-- ====================================================================
CREATE TABLE activity_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT NOT NULL,
    action_type VARCHAR(100) NOT NULL,  -- add_product, update_stock, etc.
    description TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    INDEX idx_staff (staff_id),
    INDEX idx_created (created_at)
);

-- ====================================================================
-- INSERT DEFAULT DATA
-- ====================================================================

-- Default admin staff (password: admin123)
INSERT INTO staff (username, password, email, full_name, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYsL0MCWm8u', 'admin@groceryapp.com', 'System Administrator', 'admin');

-- Default categories
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

-- Sample products
INSERT INTO products (name, category_id, description, unit_price, unit, stock_quantity) VALUES
('Red Apple', 1, 'Fresh and crispy red apples', 3.99, 'kg', 100),
('Banana', 1, 'Sweet ripe bananas', 2.49, 'kg', 150),
('Orange', 1, 'Juicy oranges', 4.99, 'kg', 80),
('Tomato', 2, 'Fresh red tomatoes', 3.49, 'kg', 120),
('Carrot', 2, 'Fresh carrots', 2.99, 'kg', 90),
('Fresh Milk', 3, 'Full cream fresh milk', 5.99, 'liter', 60),
('White Bread', 4, 'Soft white bread loaf', 2.99, 'unit', 50),
('Chicken Breast', 5, 'Boneless chicken breast', 12.99, 'kg', 40),
('Orange Juice', 6, 'Fresh orange juice', 6.99, 'liter', 70),
('Potato Chips', 7, 'Crispy salted chips', 3.99, 'pack', 100);

-- ====================================================================
-- USEFUL VIEWS
-- ====================================================================

-- Low stock products view
CREATE VIEW low_stock_products AS
SELECT p.product_id, p.name, p.stock_quantity, p.min_stock_level, c.category_name
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.stock_quantity <= p.min_stock_level
ORDER BY p.stock_quantity ASC;

-- Product sales summary
CREATE VIEW product_sales_summary AS
SELECT 
    p.product_id,
    p.name,
    c.category_name,
    COUNT(DISTINCT oi.order_id) as total_orders,
    SUM(oi.quantity) as total_quantity_sold,
    SUM(oi.subtotal) as total_revenue
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN categories c ON p.category_id = c.category_id
GROUP BY p.product_id, p.name, c.category_name;

-- User order history view
CREATE VIEW user_order_summary AS
SELECT 
    u.user_id,
    u.username,
    u.full_name,
    COUNT(o.order_id) as total_orders,
    SUM(o.final_amount) as total_spent,
    MAX(o.order_date) as last_order_date
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username, u.full_name;

-- ====================================================================
-- STORED PROCEDURES
-- ====================================================================

DELIMITER //

-- Procedure to add product to cart
CREATE PROCEDURE add_to_cart(
    IN p_user_id INT,
    IN p_product_id INT,
    IN p_quantity INT
)
BEGIN
    DECLARE current_stock INT;
    
    -- Check stock availability
    SELECT stock_quantity INTO current_stock FROM products WHERE product_id = p_product_id;
    
    IF current_stock >= p_quantity THEN
        INSERT INTO shopping_cart (user_id, product_id, quantity)
        VALUES (p_user_id, p_product_id, p_quantity)
        ON DUPLICATE KEY UPDATE quantity = quantity + p_quantity;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient stock';
    END IF;
END //

-- Procedure to place order
CREATE PROCEDURE place_order(
    IN p_user_id INT,
    IN p_delivery_address TEXT,
    IN p_delivery_phone VARCHAR(20),
    IN p_payment_method VARCHAR(20),
    OUT p_order_id INT
)
BEGIN
    DECLARE v_order_number VARCHAR(50);
    DECLARE v_total DECIMAL(10, 2);
    
    -- Generate order number
    SET v_order_number = CONCAT('ORD-', DATE_FORMAT(NOW(), '%Y%m%d'), '-', LPAD(FLOOR(RAND() * 10000), 4, '0'));
    
    -- Calculate total
    SELECT SUM(p.unit_price * sc.quantity) INTO v_total
    FROM shopping_cart sc
    JOIN products p ON sc.product_id = p.product_id
    WHERE sc.user_id = p_user_id;
    
    -- Create order
    INSERT INTO orders (user_id, order_number, total_amount, final_amount, delivery_address, delivery_phone, payment_method, order_status)
    VALUES (p_user_id, v_order_number, v_total, v_total, p_delivery_address, p_delivery_phone, p_payment_method, 'pending');
    
    SET p_order_id = LAST_INSERT_ID();
    
    -- Add order items
    INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
    SELECT p_order_id, p.product_id, p.name, sc.quantity, p.unit_price, (p.unit_price * sc.quantity)
    FROM shopping_cart sc
    JOIN products p ON sc.product_id = p.product_id
    WHERE sc.user_id = p_user_id;
    
    -- Update product stock
    UPDATE products p
    JOIN shopping_cart sc ON p.product_id = sc.product_id
    SET p.stock_quantity = p.stock_quantity - sc.quantity
    WHERE sc.user_id = p_user_id;
    
    -- Create notification
    INSERT INTO notifications (user_id, type, title, message, order_id)
    VALUES (p_user_id, 'order_placed', 'Order Placed Successfully!', 
            CONCAT('Your order ', v_order_number, ' has been placed successfully.'), p_order_id);
    
    -- Clear cart
    DELETE FROM shopping_cart WHERE user_id = p_user_id;
END //

DELIMITER ;

-- ====================================================================
-- GRANT PERMISSIONS (Optional - adjust as needed)
-- ====================================================================
-- GRANT ALL PRIVILEGES ON grocery_app_db.* TO 'root'@'localhost';
-- FLUSH PRIVILEGES;

-- ====================================================================
-- END OF SCHEMA
-- ====================================================================

SELECT 'Database grocery_app_db created successfully!' as Status;
