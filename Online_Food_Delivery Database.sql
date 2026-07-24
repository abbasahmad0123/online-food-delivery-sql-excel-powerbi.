Create Table restaurants (
	id int primary key,
	name varchar(100),
	location varchar(100)
);
Select * from restaurants;

CREATE TABLE menus (
    id INT PRIMARY KEY,
    restaurant_id INT,
    item_name VARCHAR(100),
    price DECIMAL(10,2),
    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(id)
);

CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(100)
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    restaurant_id INT,
    total DECIMAL(10,2),
    status VARCHAR(100),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

Select * from orders;

CREATE TABLE delivery_agents (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    status VARCHAR(100)
);

COPY restaurants(id, name, location)
FROM 'E:\Data Analysis Big Project\Online_Food_Delivery_Database\restaurants Table.csv'
DELIMITER ','
CSV HEADER;

Select * from restaurants;

COPY menus(id, restaurant_id, item_name, price)
FROM 'E:\Data Analysis Big Project\Online_Food_Delivery_Database\menus Table.csv'
DELIMITER ','
CSV HEADER;

Select * from menus;

COPY customers(id, name, address)
FROM 'E:\Data Analysis Big Project\Online_Food_Delivery_Database\customers Table.csv'
DELIMITER ','
CSV HEADER;

Select * from customers;

COPY orders(id, customer_id, restaurant_id, total, status)
FROM 'E:\Data Analysis Big Project\Online_Food_Delivery_Database\orders Table1.csv'
DELIMITER ','
CSV HEADER;

Select * from orders;

COPY delivery_agents(id, name, status)
FROM 'E:\Data Analysis Big Project\Online_Food_Delivery_Database\delivery_agents Table.csv'
DELIMITER ','
CSV HEADER;

Select * from orders;
Select * from delivery_agents;
Select * from customers;
Select * from menus;

SELECT
    menus.item_name,
    SUM(o.total) AS total_sold
FROM orders o
JOIN menus m
    ON orders.o_id = menus.id
GROUP BY m.item_name
ORDER BY total_sold DESC
LIMIT 3;
----01 Top 3 Food items by sales
SELECT
    m.item_name,
    SUM(o.total) AS total_sold
FROM orders o
JOIN menus m
    ON o.id = m.id
GROUP BY m.item_name
ORDER BY total_sold DESC
LIMIT 3;

----02 Count of delivery VS canclled orders
SELECT
    status,
    COUNT(*) AS total_orders
FROM orders
WHERE status IN ('Delivered', 'Cancelled', 'Out for Delivery', 'Preparing', 'Pending')
GROUP BY status;

----03 List restauarnt with most orders

SELECT
    r.id,
    r.name AS restaurant_name,
    COUNT(o.id) AS total_orders
FROM restaurants r
JOIN orders o
    ON r.id = o.restaurant_id
GROUP BY r.id, r.name
ORDER BY total_orders DESC
LIMIT 3;

----04 Assign delivery agent (join orders with agent)

SELECT
    orders.id AS order_id,
    orders.customer_id,
    orders.restaurant_id,
    delivery_agents.id AS agent_id,
    delivery_agents.name AS delivery_agent_name,
    delivery_agents.status AS agent_status,
    orders.status AS order_status
FROM orders
JOIN delivery_agents
ON orders.id = delivery_agents.id;

----05 Revenue per restaurants

SELECT
    restaurants.id,
    restaurants.name AS restaurant_name,
    SUM(orders.total) AS total_revenue
FROM restaurants
JOIN orders
ON restaurants.id = orders.restaurant_id
GROUP BY restaurants.id, restaurants.name
ORDER BY total_revenue DESC;