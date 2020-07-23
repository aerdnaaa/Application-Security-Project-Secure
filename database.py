# SQL Examples
from flaskr import file_directory
import sqlite3, os

# Connect to database
conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))

# Create cursor
c = conn.cursor()


# Create user table
# c.execute("""CREATE TABLE users (
#     username text,
#     email text,
#     password text,
#     question text,
#     answer text,
#     admin text
#     )""")
# conn.commit()
# conn.close()
# print('table created')

# Create product table
# c.execute("""CREATE TABLE products (
#     name text,
#     image text,
#     description text,
#     selling_price real,
#     cost_price real,
#     category text,
#     status text
#     )""")
# conn.commit()
# conn.close()
# print('table created')

# Create paymentdetail table
# c.execute("""CREATE TABLE paymentdetails (
#     username text,
#     name text,
#     ccnumber text,
#     expiry text,
#     cvv integer
#     )""")
# conn.commit()
# conn.close()
# print('table created')

# Create Review Table
# c.execute("""
#     CREATE TABLE reviews (
#         productid integer,
#         username text,
#         review text
#     )""")
# conn.commit()
# conn.close()
# print('table created')

# Create Vouchers Table
# c.execute("""
#     CREATE TABLE vouchers (
#         title text,
#         code text,
#         description text,
#         image_path text,
#         amount real,
#         status text,
#         used_date text,
#         user_id integer
#     )""")
# conn.commit()
# conn.close()
# print('table created')



#Create query table
# c.execute("""CREATE TABLE query (
#     name text,
#     email text,
#     subject text,
#     message text
#     )""")
# conn.commit()
# conn.close()
# print('table created')


# Insert User Voucher
# c.execute("INSERT INTO user_vouchers VALUES ('Sign Up Promo!', 'SIGNUP9012', 'You get a free $10 off voucher when you first signed up. Used the code to get $10 off your first purchase.', 10.0, 'unused', '', 1)")
# # conn.commit()
# # conn.close()
# # print('rows inserted')

# Insert User 
# c.execute("INSERT INTO users VALUES ('Admin', 'Admin@mail.com', 'admin', 'what is your mother name', 'joe','y')")
# c.execute("INSERT INTO users VALUES ('Admin2', 'Admin2@mail.com', 'password', 'what is your mother name', 'joe','y')")
# conn.commit()
# conn.close()
# print('rows inserted')


# Insert Reviews
# c.execute("INSERT INTO reviews VALUES (1, 'JohnDoe', 'Lmao this is some good stuff')")
# c.execute("INSERT INTO reviews VALUES (2, 'JohnDoe', 'this thing aint good not worth my money')")
# c.execute("INSERT INTO reviews VALUES (3, 'JohnDoe', 'useless tool. do not buy')")
# c.execute("INSERT INTO reviews VALUES (7, 'JohnDoe', 'test comment')")
# c.execute("""
# INSERT INTO reviews VALUES (4, "JohnDoe", "Your site has a problem<script>alert('XSS')</script>")
# """)
# conn.commit()
# conn.close()
# print('rows inserted')


# Insert Products
# c.execute("INSERT INTO products VALUES ('Olympic Barbell', 'products/barbell.PNG', '2.2m Olympic Barbell', 130, 50, 'barbell', 'active')")
# c.execute("INSERT INTO products VALUES ('Bench', 'products/bench.PNG', 'Incline Bench', 60, 20, 'bench', 'active')")
# c.execute("INSERT INTO products VALUES ('Half Rack', 'products/halfrack.PNG', 'Half Rack. Good for squat.', 500, 400, 'racks', 'active')")
# c.execute("INSERT INTO products VALUES ('Bumper Plates', 'products/rouge.PNG', 'Expensive bumper plates', 100, 20, 'plates', 'active')")
# c.execute("INSERT INTO products VALUES ('Squat Rack', 'products/squat.PNG', 'Cheap and good', 130, 80, 'racks', 'active')")
# c.execute("INSERT INTO products VALUES ('Flat Bench', 'products/bench2.PNG', 'Flat bench. Good for benching', 90, 45, 'bench', 'active')")
# c.execute("INSERT INTO products VALUES ('Tri-grip Plates', 'products/nyp.PNG', 'Budget plates', 100, 40, 'plates', 'active')")
# c.execute("INSERT INTO products VALUES ('Trap Bar', 'products/trap.PNG', 'Good stuff', 200, 90, 'barbell', 'inactive')")
# conn.commit()
# conn.close()
# print('rows created')


# Insert Payment details
# c.execute("INSERT INTO paymentdetails VALUES ('username', 'test', '4444444444444444', 'test', 123); DROP TABLE paymentdetails;")
# conn.commit()
# conn.close()
# print('rows created')


# Insert Voucher details
# c.execute("""
# INSERT INTO vouchers VALUES ('$10 OFF', 'vouchers/$10off.jpg', '10OFF', '$10 off your purchase', 10.0, 'active')""")
# conn.commit()
# conn.close()
# print('rows created')

# Drop User Table
# c.execute("DROP TABLE users")
# conn.commit()
# conn.close()
# print('table dropped')


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

