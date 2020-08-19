from flask import request, jsonify, redirect, url_for
from flask_restful import Resource
import sqlite3, os
from flask_login import current_user
from flaskr import file_directory
from flaskr.services.loggingservice import Logging


class Products(Resource):
    def get(self):
        try:
            admin = current_user.get_admin()
        except:
            admin = 'n'

        product_list = []
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT * FROM products ")
        products = c.fetchall()
        if admin == 'y':
            for product in products:
                product_list.append(
                    {"productName": product[1], "productImage": product[2], "productDescription": product[3],
                     "productSellingPrice": product[4], "productCostPrice": product[5], "productCategory": product[6],
                     "status": product[7], "productStock": product[8]})
        else:
            for product in products:
                if product[7] == "active":
                    product_list.append(
                        {"productName": product[1], "productImage": product[2], "productDescription": product[3],
                         "productCostPrice": product[5], "productCategory": product[6],
                         "status": product[7]})
        return jsonify(data=product_list)

    def post(self):
        try:
            admin = current_user.get_admin()
            has_account = True
        except:
            admin = 'n'
            has_account = False
        if admin == "y":
            product_name = request.form.get('productNameInput')
            product_img = request.files.get('productImage')
            product_description = request.form.get('productDescription')
            product_selling_price = request.form.get('productSellingPriceInput')
            product_cost_price = request.form.get('productCostPriceInput')
            product_category = request.form.get('productCategory')
            product_stock = request.form.get('productStock')

            # validate input to not be none
            if None in {product_name, product_img, product_description, product_selling_price, product_cost_price,
                        product_category}:
                response = jsonify(data="Missing fields.")
                response.status_code = 400
                return response

            # validate selling price and cost price
            try:
                product_selling_price = float(product_selling_price)
                product_cost_price = float(product_cost_price)
                if product_selling_price < 0 or product_cost_price < 0:
                    response = jsonify(data="Either selling price or cost price is less than 0.")
                    response.status_code = 400
                    return response
                if product_selling_price < product_cost_price:
                    response = jsonify(data="Selling price is less than cost price.")
                    response.status_code = 400
                    return response
            except:
                response = jsonify(data="Either selling price or cost price is not an integer or float.")
                response.status_code = 400
                return response

            # validate stock
            if not product_stock.isdigit():
                response = jsonify(data="Stock amount is not an positive integer.")
                response.status_code = 400
                return response
            elif product_stock == "0":
                response = jsonify(data="Stock amount cannot be 0.")
                response.status_code = 400
                return response
            else:
                product_stock = int(product_stock)

            filename = product_img.filename

            # validate filename
            if filename[-3:] not in ["png", "jpg", "peg"]:
                response = jsonify(data="Invalid file type.")
                response.status_code = 400
                return response

            filepath = 'products/' + filename
            product_img.save(os.path.join(file_directory, 'flaskr/static/img/products', filename))

            conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
            c = conn.cursor()
            c.execute("SELECT product_id from products where product_id = (select max(product_id) from products)")
            product_id = c.fetchone()[0] + 1
            c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?,'active', ?)",
                      (product_id, product_name, filepath, product_description, product_selling_price,
                       product_cost_price, product_category, product_stock))
            conn.commit()

            if request.user_agent.string[:14] != "PostmanRuntime":
                return redirect(url_for('admin.show_product'))

            return jsonify(data="Success")
        else:
            # logging
            log_type = "Unauthorized Access"
            if has_account:
                log_details = f"A user with the username {current_user.get_username()} tried to add a new product."
            else:
                log_details = "An unknown user tried to change status of a product."
            Logging(log_type, log_details)
            response = jsonify(data="You do not have authorized access to perform this action.")
            response.status_code = 401
            return response

    def put(self):
        try:
            admin = current_user.get_admin()
            has_account = True
        except:
            admin = 'n'
            has_account = False
        if admin == "y":
            request_json_data = request.get_json(force=True)

            product_name = request_json_data['product_name']
            product_status = request_json_data['product_status'].lower()

            conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
            c = conn.cursor()

            # validate product name, check if it is in database
            c.execute("SELECT * FROM products WHERE name = ?", (product_name,))
            if not c.fetchone():
                response = jsonify(f"Invalid product name, product name {product_name} not found.")
                response.status_code = 400
                return response

            # validate product status
            if product_status not in ["inactive", "active"]:
                response = jsonify("Invalid product status")
                response.status_code = 400
                return response

            c.execute("UPDATE products SET status = ? WHERE name = ?", (product_status, product_name))
            conn.commit()

            return jsonify(data="Success")
        else:
            # logging
            log_type = "Unauthorized Access"
            if has_account:
                log_details = f"A user with the username {current_user.get_username()} tried to change status of a product."
            else:
                log_details = "An unknown user tried to change status of a product."
            Logging(log_type, log_details)
            response = jsonify(data="You do not have authorized access to perform this action.")
            response.status_code = 401
            return response
