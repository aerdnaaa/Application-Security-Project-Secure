from flask import request, jsonify
from flask_restful import Resource
from flaskr import file_directory, mail
from flask_mail import Message
from flaskr.models.User import User
import sqlite3, os

class Retrieve_Password(Resource):
    def get(self):
        if request.is_json:
            email = request.json['email']
        else:
            email = request.form['email']
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute(f"SELECT * FROM users WHERE email='{email}'")
        user = c.fetchone()
        if user:
            msg = Message(f"Your password is {user[2]}", sender="andre@andre.andre", recipients=[email])
            mail.send(msg)
            return jsonify(Message=f'Password sent to {email}')
