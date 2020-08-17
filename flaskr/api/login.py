import hashlib
import os
import sqlite3

from flask import request, jsonify
from flask_login import current_user, login_user
from flask_restful import Resource
from flaskr import file_directory
from flaskr.models.User import User


class Login(Resource):
    def post(self):
        # Checks if user is logged in
        try:
            username = current_user.get_username()
            return jsonify(data="You are signed in.")
        except:
            user = None
        if request.is_json:
            username = request.json['username']
            password = request.json['password']
        else:
            username = request.form['username']
            password = request.form['password']
        if not username:
            response = jsonify({"msg": "Missing username parameter"})
            response.status_code = 400
            return response
        if not password:
            response = jsonify({"msg": "Missing password parameter"})
            response.status_code = 400
            return response
        pw_hash = hashlib.sha512(password.encode()).hexdigest()
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? and password=?", (username, pw_hash))
        user = c.fetchone()
        if user == None:
            response = jsonify(data="Incorrect email or password.")
            response.status_code = 401
        else:
            user_obj = User(user[0], user[1], user[2], user[3], user[4])
            login_user(user_obj)
            response = jsonify(data="User login successfully.")
        conn.close()
        return response
