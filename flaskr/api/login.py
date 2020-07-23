from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
import sqlite3, os
from flaskr import file_directory


class Login(Resource):
    def post(self):
        if request.is_json:
            email = request.json['email']
            password = request.json['password']
        else:
            email = request.form['email']
            password = request.form['password']
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute(f"SELECT * FROM users WHERE email='{email}'")
        test = c.fetchone()
        if test:
            access_token = create_access_token(identity=email)
            response = jsonify(message="Login succeeded!", access_token=access_token)
        else:
            response = jsonify(message="Bad email or password.")
            response.status_code = 401
        return response