import uuid


class Event:
    def __init__(self, name, date):
        self.__name = name
        self.__date = date
        self.__id = self.generate_event_id()

    @staticmethod
    def generate_event_id():
        return uuid.uuid4()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        # Add input validation
        self.__name = name

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        # Add input validation
        self.__date = date

    @property
    def id(self):
        return self.__id
