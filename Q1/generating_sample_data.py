from faker import Faker
import random
from datetime import datetime, timedelta
import sqlite3

# Connect to the database
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customer (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        address TEXT,
        phone TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product (
        product_id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProductVariant (
        variant_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        name TEXT,
        price_modifier REAL,
        FOREIGN KEY (product_id) REFERENCES Product(product_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Order (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        ship_address TEXT,
        contact_number TEXT,
        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS OrderItem (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY (order_id) REFERENCES Order(order_id),
        FOREIGN KEY (product_id) REFERENCES Product(product_id)
    )
''')

# Generate sample data

fake = Faker()

# Generate customers
num_customers = 10

for customer_id in range(1, num_customers + 1):
    name = fake.name()
    email = fake.email()
    address = fake.address().replace('\n', ', ')
    phone = fake.phone_number()

    cursor.execute('INSERT INTO Customer (customer_id, name, email, address, phone) VALUES (?, ?, ?, ?, ?)',
                   (customer_id, name, email, address, phone))

# Generate products
product_data = [
    ('iPhone', 'Apple iPhone'),
    ('Samsung Galaxy', 'Samsung Galaxy phone'),
    ('MacBook Pro', 'Apple MacBook Pro'),
    ('Dell XPS', 'Dell XPS laptop'),
    ('Sony PlayStation 5', 'Gaming console'),
    ('Samsung 4K TV', 'Samsung 4K Ultra HD TV'),
    ('Nike Air Max', 'Sports shoes'),
    ('Levi\'s Jeans', 'Denim jeans'),
    ('Fitbit Charge 4', 'Fitness tracker'),
    ('Bose QuietComfort 35 II', 'Wireless headphones')
]

for product_id, product_info in enumerate(product_data, start=1):
    name, description = product_info

    cursor.execute('INSERT INTO Product (product_id, name, description) VALUES (?, ?, ?)',
                   (product_id, name, description))

# Generate product variants
product_variants = [
    (1, '64GB', 0),
    (1, '128GB', 100),
    (6, '55"', 0),
    (6, '65"', 200),
]

for variant_id, variant_info in enumerate(product_variants, start=1):
    product_id, name, price_modifier = variant_info

    cursor.execute('INSERT INTO ProductVariant (variant_id, product_id, name, price_modifier) VALUES (?, ?, ?, ?)',
                   (variant_id, product_id, name, price_modifier))

# Generate orders
start_date = datetime.now() - timedelta(days=2 * 365)  # 2 years of order history
end_date = datetime.now()
num_days = (end_date - start_date).days

order_id = 1

for customer_id in range(1, num_customers + 1):
    num_orders = random.randint(5, 20)

    for _ in range(num_orders):
        order_date = start_date + timedelta(days=random.randint(0, num_days))
        ship_address = fake.address().replace('\n', ', ')
        contact_number = fake.phone_number()

        cursor.execute('INSERT INTO Order (order_id, customer_id, order_date, ship_address, contact_number) VALUES (?, ?, ?, ?, ?)',
                       (order_id, customer_id, order_date.strftime('%Y-%m-%d'), ship_address, contact_number))

        num_order_items = random.randint(1, 5)

        for _ in range(num_order_items):
            product_id = random.randint(1, len(product_data))
            quantity = random.randint(1, 10)
            price = random.uniform(10, 1000)

            cursor.execute('INSERT INTO OrderItem (order_item_id, order_id, product_id, quantity, price) VALUES (?, ?, ?, ?, ?)',
                           (order_id, order_id, product_id, quantity, price))

            order_id += 1

# Commit the changes and close the connection
conn.commit()
conn.close()
