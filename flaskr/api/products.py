from flask import request, jsonify, redirect, url_for
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_claims, get_jwt_identity, jwt_required
import sqlite3, os
from flaskr import file_directory


class Products(Resource):
    @jwt_optional
    def get(self):
        identity = get_jwt_identity()
        if identity:
            claims = get_jwt_claims()
            admin = claims['admin']
        else:
            admin = 'n'
        product_list = []
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute(f"SELECT * FROM products ")
        products = c.fetchall()
        if admin == 'y':
            for product in products:
                product_list.append(
                    {"productName": product[0], "productImage": product[1], "productDescription": product[2],
                     "productSellingPrice": product[3], "productCostPrice": product[4], "productCategory": product[5],
                     "status": product[6]})
        else:
            for product in products:
                if product[6] == "active":
                    product_list.append(
                        {"productName": product[0], "productImage": product[1], "productDescription": product[2],
                         "productCostPrice": product[4], "productCategory": product[5],
                         "status": product[6]})
        return jsonify(data=product_list)

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        admin = claims["admin"]
        if admin == "y":
            product_name = request.form.get('productNameInput')
            product_img = request.files.get('productImage')
            product_description = request.form.get('productDescription')
            product_selling_price = request.form.get('productSellingPriceInput')
            product_cost_price = request.form.get('productCostPriceInput')
            product_category = request.form.get('productCategory')

            # validate input to not be none
            if None in {product_name, product_img, product_description, product_selling_price, product_cost_price, product_category}:
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
            c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?,'active')",
                (product_name, filepath, product_description, product_selling_price, product_cost_price, product_category))
            conn.commit()

            if request.user_agent.string[:14] != "PostmanRuntime":
                return redirect(url_for('admin.show_product'))

            return jsonify(data="Success")
        else:
            # need to log
            response = jsonify(data="You do not have authorized access to perform this action.")
            response.status_code = 401
            return response

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        admin = claims["admin"]
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
            # need to log
            response = jsonify(data="You do not have authorized access to perform this action.")
            response.status_code = 401
            return response
