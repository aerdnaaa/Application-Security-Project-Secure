class Logging:
    def __init__(self, id, LogDetails, LogType, LogDateTime ):
        self.__id = id
        self.__LogDetails = LogDetails
        self.__LogType = LogType
        self.__LogDateTime = LogDateTime

    def get_id(self):
        return self.__id
    def set_id(self,id):
        self.__id = id
    def get_LogDetails(self):
        return self.__LogDetails
    def set_LogDetails(self,LogDetails):
        self.__LogDetails = LogDetails
    def get_LogType(self):
        return self.__LogType
    def set_LogType(self,LogType):
        self.__LogType = LogType
    def get_LogDateTime(self):
        return self.__LogDateTime
    def set_LogDateTime(self,LogDateTime):
        self.__LogDateTime = LogDateTime