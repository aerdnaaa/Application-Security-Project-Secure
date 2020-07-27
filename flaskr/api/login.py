from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
import sqlite3, os
import hashlib
from flaskr import file_directory


class Login(Resource):
    def post(self):
        if request.is_json:
            email = request.json['email']
            password = request.json['password']
        else:
            email = request.form['email']
            password = request.form['password']
        if not email:
            response = jsonify({"msg":"Missing username parameter"})
            response.status_code = 400
            return response
        if not password:
            response = jsonify({"msg": "Missing password parameter"})
            response.status_code = 400
            return response
        pw_hash = hashlib.sha512(password.encode()).hexdigest()
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? and password=?", (email, pw_hash))
        test = c.fetchone()
        if test:
            username = test[0]
            access_token = create_access_token(identity=username)
            response = jsonify(message="Login succeeded!", access_token=access_token)
        else:
            response = jsonify(message="Bad email or password.")
            response.status_code = 401
        return response