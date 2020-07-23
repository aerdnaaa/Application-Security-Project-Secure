class Product:
    def __init__(self, name, image, description, selling_price, cost_price, category, status):
        self.__name = name
        self.__image = image
        self.__description = description
        self.__selling_price = selling_price
        self.__cost_price = cost_price
        self.__category = category
        self.__status = status

    def get_name(self):
        return self.__name

    def get_image(self):
        return self.__image

    def get_description(self):
        return self.__description

    def get_selling_price(self):
        return self.__selling_price

    def get_cost_price(self):
        return self.__cost_price

    def get_category(self):
        return self.__category

    def get_status(self):
        return self.__status
