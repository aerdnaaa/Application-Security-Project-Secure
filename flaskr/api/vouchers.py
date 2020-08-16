from flask import request, jsonify, redirect, url_for
from flask_restful import Resource
import sqlite3, os
from flask_login import current_user
from flaskr import file_directory
from flaskr.services.loggingservice import Logging


class Vouchers(Resource):
    def get(self):
        try:
            is_admin = current_user.get_admin()
        except:
            is_admin = 'n'
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM vouchers where user_id=0")
        conn.commit()
        if is_admin == 'y':
            vouchers = [dict(row) for row in c.fetchall()]
        else:
            vouchers = []
            for row in c.fetchall():
                if row[5] == "active":
                    vouchers.append(dict(row))
            conn.close()

        return jsonify(data=vouchers)

    def post(self):
        try:
            identity = current_user.get_username()
            admin = current_user.get_admin()
            has_account = True
        except:
            identity = None
            admin = 'n'
            has_account = False
        if admin == "y":
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

            # validate if voucher title is in database
            c.execute("SELECT * FROM vouchers WHERE title=?", (voucher_title,))
            if c.fetchone():
                response = jsonify(data="Voucher Title is used.")
                response.status_code = 400
                return response

            # validate if voucher code is in database
            c.execute("SELECT * FROM vouchers WHERE code=?", (voucher_code,))
            if c.fetchone():
                response = jsonify(data="Voucher Code is used.")
                response.status_code = 400
                return response

            # validate input to not be none
            if None in {voucher_title, voucher_code, voucher_img, voucher_description, voucher_amount}:
                response = jsonify(data="Missing fields.")
                response.status_code = 400
                return response

            # prevent sql injection
            c.execute("INSERT INTO vouchers VALUES (?, ?, ?, ?, ?, 'active', '', 0)",
                      (voucher_title, voucher_code, voucher_description, filepath, voucher_amount))
            conn.commit()

            if request.user_agent.string[:14] != "PostmanRuntime":
                return redirect(url_for('admin.show_voucher'))

            return jsonify(data="Success. Voucher Created.")
        else:
            # logging
            log_type = "Unauthorized Access"
            if has_account:
                log_details = f"A user with the username {identity} tried to add a new voucher."
            else:
                log_details = f"Am unknown user tried to add a new voucher."
            Logging(log_type, log_details)
            response = jsonify(data="You do not have authorized access to perform this action.")
            response.status_code = 401
            return response

    def put(self):
        try:
            identity = current_user.get_username()
            admin = current_user.get_admin()
            has_account = True
        except:
            identity = None
            admin = 'n'
            has_account = False
        if admin == "y":
            conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
            c = conn.cursor()

            request_json_data = request.get_json(force=True)
            voucher_name = request_json_data['voucher_name']
            voucher_status = request_json_data['voucher_status'].lower()

            # validate voucher_name
            c.execute("SELECT * FROM vouchers WHERE title=?", (voucher_name,))
            if not c.fetchone():
                response = jsonify(data="No such Voucher Title.")
                response.status_code = 400
                return response

            # validate voucher_status
            if voucher_status not in ["active", "inactive"]:
                response = jsonify(data="Invalid voucher status.")
                response.status_code = 400
                return response

            # prevent sql injection
            c.execute("UPDATE vouchers SET status = ? WHERE title = ?", (voucher_status, voucher_name, ))
            conn.commit()

            return jsonify(data="Success. Voucher Status Updated.")
        else:
            # logging
            log_type = "Unauthorized Access"
            if has_account:
                log_details = f"A user with the username {identity} tried to change status of voucher."
            else:
                log_details = "An unknown user tried to change status of a voucher."
            Logging(log_type, log_details)
            response = jsonify(data="Unauthorized access")
            response.status_code = 401
            return response
