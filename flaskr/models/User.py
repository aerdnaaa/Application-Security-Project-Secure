class User:

    def __init__(self, username, email, password, question, answer):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__question = question
        self.__answer = answer
        self.__voucher = ""

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_question(self):
        return self.__question

    def get_answer(self):
        return self.__answer

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_voucher(self, voucher):
        self.__voucher = voucher