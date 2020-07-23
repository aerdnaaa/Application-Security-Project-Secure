import uuid, shelve


class AddressObj:

    def __init__(self, name, address, postal):
        self.set_id()
        self.__name = name
        self.__address = address
        self.__postal = postal

    def set_id(self):
        while True:
            id = str(uuid.uuid4())
            if id[0] in '1234567890':
                id = str(uuid.uuid4())
            else:
                break
        self.__id = id

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    def get_postal(self):
        return self.__postal

    def set_postal(self, postal):
        self.__postal = postal


