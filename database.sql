-- Create schema
CREATE SCHEMA erp;

-- Create a basic product table
CREATE TABLE erp.product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    image VARCHAR(100),
    tags VARCHAR(200)
);

-- Create a basic combo/gift set table
CREATE TABLE erp.combo (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    image VARCHAR(100)
);

-- Create relationship between combos and their included products
CREATE TABLE erp.combo_product (
    id SERIAL PRIMARY KEY,
    combo_id INTEGER REFERENCES erp.combo(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES erp.product(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1
);

-- Create a cart table for tracking user sessions
CREATE TABLE erp.cart_item (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    product_id INTEGER REFERENCES erp.product(id) ON DELETE SET NULL,
    combo_id INTEGER REFERENCES erp.combo(id) ON DELETE SET NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (product_id IS NOT NULL OR combo_id IS NOT NULL)
);

-- Create a chat history table for the AI recommendations
CREATE TABLE erp.chat_history (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);