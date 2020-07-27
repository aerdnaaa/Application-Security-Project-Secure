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

            filename = product_img.filename
            filepath = 'products/' + filename
            product_img.save(os.path.join(file_directory, 'flaskr/static/img/products', filename))

            conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
            c = conn.cursor()
            c.execute(
                f"INSERT INTO products VALUES ('{product_name}', '{filepath}', '{product_description}', '{product_selling_price}', '{product_cost_price}', '{product_category}','active')")
            conn.commit()

            if request.user_agent.string[:14] != "PostmanRuntime":
                return redirect(url_for('admin.show_product'))

            return jsonify(data="Success")
        else:
            response = jsonify(data="Unauthorized access")
            response.status_code = 401
            return response

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        admin = claims["admin"]
        if admin == "y":
            request_json_data = request.get_json(force=True)

            product_name = request_json_data['product_name']
            product_status = request_json_data['product_status']

            conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
            c = conn.cursor()
            c.execute(f"UPDATE products SET status = '{product_status}' WHERE name = '{product_name}'")
            conn.commit()

            return jsonify(data="Success")
        else:
            response = jsonify(data="Unauthorized access")
            response.status_code = 401
            return response
