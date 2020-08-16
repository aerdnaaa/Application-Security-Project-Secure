# SQL Examples
import hashlib
import os
import sqlite3
import pyffx

from flaskr import file_directory

# Connect to database
conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))

# Create cursor
c = conn.cursor()


# Create all the tables
def create_tables():
    # Create log table
    c.execute("""CREATE TABLE IF NOT EXISTS logs (
        log_id integer primary key autoincrement,
        log_details text,
        log_type text,
        log_date_time varchar
        )""")
    print('logs table created')

    # Create user table
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id integer primary key,
        username text,
        email text,
        password text,
        admin text
        )""")
    print('users table created')

    # Create product table
    c.execute("""CREATE TABLE IF NOT EXISTS products (
        product_id integer primary key,
        name text,
        image text,
        description text,
        selling_price real,
        cost_price real,
        category text,
        status text,
        stock_level integer
        )""")
    print('products table created')

    # Create paymentdetail table
    c.execute("""CREATE TABLE IF NOT EXISTS paymentdetails (
        user_id integer,
        name text,
        credit_card_number text,
        expiry text,
        cvv integer,
        FOREIGN KEY (user_id)
            references users (user_id)
            on update cascade 
            on delete cascade 
        )""")
    print('paymentdetail table created')

    # Create reviews Table
    c.execute("""CREATE TABLE IF NOT EXISTS reviews (
            product_id integer,
            username text,
            review text,
            FOREIGN KEY (product_id)
                references products (product_id)
                on update cascade
                on delete cascade
        )""")
    print('reviews table created')

    # Create vouchers Table
    c.execute("""CREATE TABLE IF NOT EXISTS vouchers (
            title text,
            code text unique,
            description text,
            image_path text,
            amount real,
            status text,
            used_date text,
            user_id integer,
            FOREIGN KEY (user_id)
                references users (user_id)
                on update cascade 
                on delete cascade 
        )""")
    print('vouchers table created')

    # Create query table
    c.execute("""CREATE TABLE IF NOT EXISTS query (
        name text,
        email text,
        subject text,
        message text
        )""")
    print('query table created')


def add_sample_data():
    pw_hash = hashlib.sha512("Admin@123456".encode()).hexdigest()

    # Insert Account with admin id 0
    c.execute("""INSERT INTO users VALUES (0, 'nil', 'nil', '', 'n')""")

    # Insert Admin Account
    c.execute("""INSERT INTO users VALUES (590, 'Admin', 'Admin@mail.com', ?, 'y')""", (pw_hash,))
    c.execute("""INSERT INTO users VALUES (324, 'Admin2', 'Admin@mail.com', ?, 'y')""", (pw_hash,))
    print('insert admin account into table')

    # Insert User Account
    c.execute("""INSERT INTO users VALUES (999, 'Andre', 'Andre@mail.com', ?, 'n')""", (pw_hash,))
    c.execute("""INSERT INTO users VALUES (333, 'Jooseng', 'Jooseng@mail.com', ?, 'n')""", (pw_hash,))
    print('insert user account into table')

    # Insert Products
    c.execute(
        "INSERT INTO products VALUES (1, 'Olympic Barbell', 'products/barbell.PNG', '2.2m Olympic Barbell', 130, 50, 'barbell', 'active', 100)")
    c.execute(
        "INSERT INTO products VALUES (2, 'Bench', 'products/bench.PNG', 'Incline Bench', 60, 20, 'bench', 'active', 200)")
    c.execute(
        "INSERT INTO products VALUES (3, 'Half Rack', 'products/halfrack.PNG', 'Half Rack. Good for squat.', 500, 400, 'racks', 'active', 300)")
    c.execute(
        "INSERT INTO products VALUES (4, 'Bumper Plates', 'products/rouge.PNG', 'Expensive bumper plates', 100, 20, 'plates', 'active', 200)")
    c.execute(
        "INSERT INTO products VALUES (5, 'Squat Rack', 'products/squat.PNG', 'Cheap and good', 130, 80, 'racks', 'active', 300)")
    c.execute(
        "INSERT INTO products VALUES (6, 'Flat Bench', 'products/bench2.PNG', 'Flat bench. Good for benching', 90, 45, 'bench', 'active', 200)")
    c.execute(
        "INSERT INTO products VALUES (7, 'Tri-grip Plates', 'products/nyp.PNG', 'Budget plates', 100, 40, 'plates', 'active', 300)")
    c.execute(
        "INSERT INTO products VALUES (8, 'Trap Bar', 'products/trap.PNG', 'Good stuff', 200, 90, 'barbell', 'inactive', 200)")
    print('insert products into table')

    # Insert Reviews
    c.execute("INSERT INTO reviews VALUES (1, 'JohnDoe', 'Lmao this is some good stuff')")
    c.execute("INSERT INTO reviews VALUES (2, 'JohnDoe', 'this thing aint good not worth my money')")
    c.execute("INSERT INTO reviews VALUES (3, 'JohnDoe', 'useless tool. do not buy')")
    c.execute("INSERT INTO reviews VALUES (7, 'JohnDoe', 'test comment')")
    print('insert reviews into table')

    # Insert payment details
    credit_card_1 = '4000111122223333'
    cvv_1 = 432
    e1 = pyffx.Integer(b'12376987ca98sbdacsbjkdwd898216jasdnsd98213912', length=16)
    e2 = pyffx.Integer(b'12376987ca98sbdacsbjkdwd898216jasdnsd98213912', length=3)
    encrypted_card_no = e1.encrypt(credit_card_1)
    encrypted_card_cvv = e2.encrypt(cvv_1)
    c.execute("INSERT INTO paymentdetails VALUES (999, 'Andre Goh', ?, '2022-01-01', ?)",
              (encrypted_card_no, encrypted_card_cvv))
    credit_card_2 = '5555111122223333'
    cvv_2 = 562
    encrypted_card_no = e1.encrypt(credit_card_2)
    encrypted_card_cvv = e2.encrypt(cvv_2)
    c.execute("INSERT INTO paymentdetails VALUES (999, 'Andre Goh', ?, '2022-01-01', ?)",
              (encrypted_card_no, encrypted_card_cvv))
    print("insert payment details into table")

    # Insert vouchers
    c.execute(
        "INSERT INTO vouchers VALUES ('$20 OFF', '$20OFF', '20 dollars off coupon for any purchase.', 'vouchers/c16935324831acb66f8b4b1395fcefbd.png', 20, 'active', '', 0)")
    c.execute(
        "INSERT INTO vouchers VALUES ('$10 OFF', '10OFF', '$10 off your purchase', 'vouchers/$10off.jpg', 10.0, 'active', '', 0)")
    print("insert vouchers into table")

create_tables()
add_sample_data()
conn.commit()
conn.close()

# Insert Payment details
# c.execute("INSERT INTO paymentdetails VALUES ('username', 'test', '4444444444444444', 'test', 123); DROP TABLE paymentdetails;")
# conn.commit()
# conn.close()
# print('rows created')




# Drop Product Table
# c.execute("DROP TABLE products")
# conn.commit()
# conn.close()
# print('table dropped')


# Drop Payment details Table
# c.execute("DROP TABLE paymentdetails")
# conn.commit()
# conn.close()
# print('table dropped')

# Drop Review Table
# c.execute("DROP TABLE reviews")
# conn.commit()
# conn.close()
# print('table dropped')


# Drop Voucher Table
# c.execute("DROP TABLE reviews")
# conn.commit()
# conn.close()
# print('table dropped')


# Query DB
# c.execute("SELECT rowid, * FROM products WHERE name LIKE '%{}%'".format("' UNION SELECT '1', sql, '3', '4', '5', '6' FROM sqlite_master--"))
# c.execute("SELECT rowid, * FROM products WHERE name LIKE '%''%' UNION SELECT * FROM x--")
# print(c.fetchall())
# conn.close()

# c.execute("SELECT * FROM reviews")
# print(c.fetchall())

# c.execute("""SELECT * FROM users WHERE username='Admin' AND password='admin' """)
# print(c.fetchone())

# To see table names
# c.execute(" SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
# print(c.fetchall())

# c.execute("SELECT name FROM (SELECT * FROM sqlite_master UNION ALL SELECT * FROM sqlite_temp_master) WHERE type='table' ORDER BY name")
# print(c.fetchone())

# See all tables created in sqlite db
# c.execute("SELECT * FROM users WHERE username='' UNION SELECT sql, '2', '3', '4', '5' FROM sqlite_master-- ")
# print(c.fetchone())


# setting admin status
# c.execute("update users set admin ='y' where username='Admin'")
# conn.commit()
# conn.close()
# print('table updated')
