# FLASK LOGIN
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, username, email, password, admin):
        self.id = id
        self.__username = username
        self.__email = email
        self.__password = password
        self.__admin = admin

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_admin(self):
        return self.__admin

