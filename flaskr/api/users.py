from flask import request, jsonify
from flask_restful import Resource
import sqlite3, os
from flaskr import file_directory


class Users(Resource):
    def get(self):
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        conn.commit()
        user = c.fetchall()
        conn.close()
        print(user)

    def post(self):
        email = request.get_json()['email']
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute(f"SELECT * FROM users WHERE email='{email}'")
        test = c.fetchone()
        if test:
            response = jsonify(message="That email already exists.")
            response.status_code = 409
        else:
            username = request.get_json()['username']
            password = request.get_json()['password']
            question = request.get_json()['question']
            answer = request.get_json()['answer']
            c.execute(f"INSERT INTO users VALUES ('{username}', '{email}', '{password}', '{question}', '{answer}')")
            conn.commit()
            conn.close()
            response = jsonify(message="User created successfully.")
            response.status_code = 201
        return response
