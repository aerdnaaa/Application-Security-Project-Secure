import uuid, datetime, shelve


class object:
    def set_id(self):
        while True:
            id = str(uuid.uuid4())
            if id[0] in '1234567890':
                id = str(uuid.uuid4())
            else:
                break
        self.__id = id

    def __init__(self):
        self.set_id()

    def get_id(self):
        return self.__id


class Addpdtobj(object):
    def __init__(self, product, image, quantity, category, description, price, costPrice):
        super().__init__()
        self.__sold = 0
        self.__product = product
        self.__image = image
        self.__quantity = quantity
        self.__description = description
        self.__category = category
        self.__price = price
        self.__costPrice = costPrice

    # Accessor Methods
    def get_sold(self):
        return self.__sold

    def get_product(self):
        return self.__product

    def get_image(self):
        return self.__image

    def get_quantity(self):
        return self.__quantity

    def get_description(self):
        return self.__description

    def get_category(self):
        return self.__category

    def get_price(self):
        return self.__price

    def get_costPrice(self):
        return self.__costPrice

    # Mutator Methods
    def set_product(self, product):
        self.__product = product

    def set_sold(self, sold):
        self.__sold = sold

    def set_image(self, image):
        self.__image = image

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_description(self, description):
        self.__description = description

    def set_category(self, category):
        self.__category = category

    def set_price(self, price):
        self.__price = price

    def set_costPrice(self, costPrice):
        self.__costPrice = costPrice


class FAQobj(object):
    def __init__(self, title, answer):
        super().__init__()
        self.__title = title
        self.__answer = answer

    # Accessor Methods
    def get_title(self):
        return self.__title

    def get_answer(self):
        return self.__answer

    # Mutator Methods
    def set_title(self, title):
        self.__title = title

    def set_answer(self, answer):
        self.__answer = answer


class ContactUsobj(object):
    def __init__(self, name, email, subject, message):
        super().__init__()
        self.__date = datetime.datetime.now().strftime("%d") + ' ' + datetime.datetime.now().strftime(
            "%b") + ' ' + datetime.datetime.now().strftime("%Y")
        self.__name = name
        self.__email = email
        self.__subject = subject
        self.__message = message

    # Accessor Methods
    def get_date(self):
        return self.__date

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_subject(self):
        return self.__subject

    def get_message(self):
        return self.__message


class galleryobj(object):
    def __init__(self, image, title, subtitle):
        super().__init__()
        self.__image = image
        self.__status = "inactive"
        self.__title = title
        self.__subtitle = subtitle

    # Accessor Methods
    def get_image(self):
        return self.__image

    def get_status(self):
        return self.__status

    def get_title(self):
        return self.__title

    def get_subtitle(self):
        return self.__subtitle

    # Mutator Methods
    def set_image(self, image):
        self.__image = image

    def set_status(self, status):
        self.__status = status

    def set_title(self, title):
        self.__title = title

    def set_subtitle(self, subtitle):
        self.__subtitle = subtitle


class AddDealsObj():
    def __init__(self, promocode, promotype, startdate, expirydate):
        self.__promocode = promocode
        self.__promotype = promotype
        self.__startdate = startdate
        self.__expirydate = expirydate
        self.__status = ""

    def get_promocode(self):
        return self.__promocode

    def get_promotype(self):
        return self.__promotype

    def get_expirydate(self):
        return self.__expirydate

    def get_startdate(self):
        return self.__startdate

    def get_status(self):
        return self.__status

    def set_promocode(self, promocode):
        self.__promocode = promocode

    def set_promotype(self, promotype):
        self.__promotype = promotype

    def set_expirydate(self, expirydate):
        self.__expirydate = expirydate

    def set_startdate(self, startdate):
        self.__startdate = startdate

    def set_Inactive(self):
        self.__status = 'Inactive'

    def set_Active(self):
        self.__status = 'Active'
