import uuid
class PaymentInfo:
    def set_id(self):
        while True:
            id = str(uuid.uuid4())
            if id[0] in '1234567890':
                id = str(uuid.uuid4())
            else:
                break
        self.__id = id
    
    def __init__(self, FullName , CreditCardNo , expiryDate, ccv ):
        self.set_id()
        self.__Fullname = FullName
        self.__CreditCardNo = CreditCardNo
        self.__expiryDate = expiryDate
        self.__ccv = ccv

    def get_id(self):
        return self.__id

    def get_full_name(self):
        return self.__Fullname

    def get_credit_card_number(self):
        return self.__CreditCardNo

    def get_expiry_date(self):
        return self.__expiryDate

    def get_ccv(self):
        return self.__ccv

    def set_full_name(self, value):
        self.__FullName = value

    def set_credit_card_number(self, value):
        self.__CreditCardNo = value

    def set_expiryDate(self, value):
        self.__expiryDate = value

    def set_ccv(self, value):
        self.__ccv = value