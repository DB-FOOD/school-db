-- see ordered items for a particular order

-- see orders for a particular customer (not only order_id but items ordered)

-- ordered items at a particular date

-- Get all customers
SELECT * FROM customers;

-- Insert a new customer
INSERT INTO customers (name, address, city, country) 
VALUES ($1, $2, $3, $4) RETURNING *;
