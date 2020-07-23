import shelve, uuid
from datetime import date, timedelta, datetime


class OrderObj:
    def __init__(self, product, quantity, username, paid, address, postal, name, promo, gateway):
        # Accept list of product obj
        self.__product = product
        # Accept list of product quantity
        self.__quantity = quantity

        # Normal Order details
        self.__username = username
        self.__paid = paid
        self.__orderId = str(uuid.uuid4())
        self.__status = "Pending Approval"
        self.__dateDisplay = datetime.now().strftime("%d") + ' ' + datetime.now().strftime(
            "%b") + ' ' + datetime.now().strftime("%Y")
        self.__invoice = ""
        self.__remove = False
        self.__address = address
        self.__postal = postal
        self.__name = name
        self.__promo = promo
        self.__gateway = gateway

    def get_username(self):
        return self.__username

    def get_paid(self):
        return self.__paid

    def get_quantity(self):
        return self.__quantity

    def get_product(self):
        return self.__product

    def get_orderId(self):
        return self.__orderId

    def get_status(self):
        return self.__status

    def get_dateDisplay(self):
        return self.__dateDisplay

    def get_invoice(self):
        return self.__invoice

    def get_remove(self):
        return self.__remove

    def get_promo(self):
        return self.__promo

    def get_address(self):
        return self.__address

    def get_postal(self):
        return self.__postal

    def get_name(self):
        return self.__name

    def get_gateway(self):
        return self.__gateway

    def set_status(self, status):
        self.__status = status

    def set_dateDisplay(self, date):
        self.__dateDisplay = date

    def set_invoice(self, invoice):
        self.__invoice = invoice

    def set_remove(self, remove):
        self.__remove = remove

    def set_promo(self, promo):
        self.__promo = promo

# db = shelve.open('storage.db', 'w')
# db['orders'] = {}
# db.close()
