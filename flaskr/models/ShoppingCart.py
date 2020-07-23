import uuid


class ShoppingCartObj:

    def __init__(self, product):
        self.__product = product
        self.__quantity = 1
        self.__promo = ""

    def set_product(self, product):
        self.__product = product

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_promo(self, promo):
        self.__promo = promo

    def get_product(self):
        return self.__product

    def get_quantity(self):
        return self.__quantity

    def get_promo(self):
        return self.__promo