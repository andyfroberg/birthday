import uuid
from abc import ABC

class Event(ABC):
    def __init__(self, date):
        self.__date = date
        self.__id = self.generate_event_id()

    @staticmethod
    def generate_event_id():
        return uuid.uuid4()

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def id(self):
        return self.__id

class NameAndDateEvent(Event):
    """
    Event that has a name tied to the date.
    Anniversaries, birthdays or holiday's.
    """
    
    def __init__(self, date, name):
        super().__init__(date)
        self.__name = name
    
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
    
class DescriptionEvent(Event):
    """For any other kind of event reminders, like interview, get together, etc."""
    
    def __init__(self, date, title, description):
        super().__init__(date)
        self.__title = title
        self.__description = description
    
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title
    
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__name = description
