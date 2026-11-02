
-- Create Pizza Types Table
CREATE TABLE pizza_types (
    pizza_type_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    ingredients TEXT
);

-- Create Pizzas Table
CREATE TABLE pizzas (
    pizza_id VARCHAR(50) PRIMARY KEY,
    pizza_type_id VARCHAR(50) REFERENCES pizza_types(pizza_type_id),
    pizza_size VARCHAR(10),
    price NUMERIC(10,2)
);

-- Create Orders Table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    order_date DATE,
    order_time TIME
);

-- Create Order Details Table
CREATE TABLE order_details (
    order_details_id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    pizza_id VARCHAR(50) REFERENCES pizzas(pizza_id),
    quantity INTEGER
);
