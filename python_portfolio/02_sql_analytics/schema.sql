PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL CHECK (unit_price >= 0)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date TEXT NOT NULL
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0)
);

INSERT INTO customers VALUES
(1, 'Customer A', 'North'),
(2, 'Customer B', 'South'),
(3, 'Customer C', 'West'),
(4, 'Customer D', 'East');

INSERT INTO products VALUES
(1, 'Keyboard', 'Accessories', 45.0),
(2, 'Mouse', 'Accessories', 25.0),
(3, 'Monitor', 'Electronics', 220.0),
(4, 'Notebook', 'Stationery', 4.5);

INSERT INTO orders VALUES
(101, 1, '2025-01-12'),
(102, 2, '2025-01-18'),
(103, 1, '2025-02-03'),
(104, 3, '2025-02-20'),
(105, 4, '2025-03-08'),
(106, 2, '2025-03-22');

INSERT INTO order_items VALUES
(1, 101, 1, 2, 45.0),
(2, 101, 2, 1, 25.0),
(3, 102, 3, 1, 220.0),
(4, 103, 2, 3, 25.0),
(5, 104, 4, 10, 4.5),
(6, 104, 1, 1, 45.0),
(7, 105, 3, 2, 220.0),
(8, 106, 4, 20, 4.5),
(9, 106, 2, 2, 25.0);
