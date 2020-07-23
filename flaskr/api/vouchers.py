from flask import request, jsonify, redirect, url_for
from flask_restful import Resource
import sqlite3, os
from flaskr import file_directory


class Vouchers(Resource):
    def get(self):
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(f"SELECT * FROM vouchers where user_id=0")
        conn.commit()
        vouchers = [dict(row) for row in c.fetchall()]
        conn.close()

        print(vouchers)

        return jsonify(data=vouchers)

    def post(self):
        voucher_title = request.form.get('voucherNameInput')
        voucher_code = request.form.get('voucherCode')
        voucher_img = request.files.get('voucherImage')
        voucher_description = request.form.get('voucherDescription')
        voucher_amount = request.form.get('voucherAmountInput')

        filename = voucher_img.filename
        filepath = 'vouchers/' + filename
        voucher_img.save(os.path.join(file_directory, 'flaskr/static/img', filepath))

        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()

        # Validate if voucher title is in database
        c.execute(f"SELECT * FROM vouchers WHERE title='{voucher_title}'")
        if c.fetchone():
            response = jsonify(data="Voucher Title is used.")
            response.status_code = 400
            return response

        # Validate if voucher code is in database
        c.execute(f"SELECT * FROM vouchers WHERE code='{voucher_code}'")
        if c.fetchone():
            response = jsonify(data="Voucher Code is used.")
            response.status_code = 400
            return response

        c.execute(
            f"INSERT INTO vouchers VALUES ('{voucher_title}', '{voucher_code}', '{voucher_description}', '{filepath}', '{voucher_amount}', 'active', '', 0)")
        conn.commit()

        if request.user_agent.string[:14] != "PostmanRuntime":
            return redirect(url_for('admin.show_voucher'))

        return jsonify(data="Success. Voucher Created.")

    def put(self):
        request_json_data = request.get_json(force=True)

        voucher_name = request_json_data['voucher_name']
        voucher_status = request_json_data['voucher_status']

        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute(f"UPDATE vouchers SET status = '{voucher_status}' WHERE title = '{voucher_name}'")
        conn.commit()

        return jsonify(data="Success. Voucher Status Updated.")
