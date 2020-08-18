import os
import random
import sqlite3
import string

from flask import request, jsonify
from flask_login import current_user
from flask_restful import Resource
from flaskr import file_directory
from flaskr.services.loggingservice import Logging


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


class UserVoucher(Resource):
    def get(self, user_id):
        try:
            identity = str(current_user.id)
            has_account = True
        except:
            identity = 'none'
            has_account = False

        if identity != user_id:
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
        else:
            conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM vouchers WHERE user_id = ?", (user_id,))
            conn.commit()
            vouchers = [dict(row) for row in c.fetchall()]
            conn.close()

            return jsonify(data=vouchers)

    def post(self, user_id):
        try:
            admin = current_user.get_admin()
            has_account = True
        except:
            admin = 'n'
            has_account = False
        if admin == 'y':
            conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
            c = conn.cursor()

            request_json_data = request.get_json(force=True)
            voucher_title = request_json_data["title"]
            # Validate if voucher code is in database
            while True:
                voucher_code = get_random_alphanumeric_string(8)
                c.execute(f"SELECT * FROM vouchers WHERE code='{voucher_code}'")
                if not c.fetchone():
                    break
            voucher_image = ""
            voucher_description = request_json_data["description"]
            voucher_amount = request_json_data["amount"]
            voucher_status = "unused"
            used_date = ""

            c.execute("INSERT INTO vouchers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (voucher_title, voucher_code, voucher_description, voucher_image, voucher_amount, voucher_status,
                       used_date, user_id))
            conn.commit()
            conn.close()

            return jsonify(data="Voucher created with user id of {}".format(user_id))
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

    def put(self, user_id):
        try:
            identity = str(current_user.id)
            has_account = True
        except:
            identity = None
            has_account = False
        if user_id == identity:
            import datetime
            request_json_data = request.get_json(force=True)
            code = request_json_data["code"]
            used_date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

            conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
            c = conn.cursor()
            c.execute("SELECT * FROM vouchers WHERE code = ? AND status = 'unused'", (code,))

            if c.fetchone():
                c.execute("UPDATE vouchers SET status = 'used', used_date = ? WHERE code = ?", (used_date, code,))
                conn.commit()
                conn.close()

                return jsonify(data=f"Voucher with the code {code} from username {user_id} has been used.")

            else:
                c.execute("SELECT * FROM vouchers WHERE code=? AND user_id=0", (code,))
                if c.fetchone():
                    conn.commit()
                    conn.close()
                    return jsonify(data="This is a general voucher")
                else:
                    conn.commit()
                    conn.close()

                    return jsonify(data=f"Voucher with the code {code} from username {user_id} has already been used.")
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
