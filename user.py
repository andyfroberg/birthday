

class User:
    def __init__(self, username, email, events={}):
        self.__username = username
        self.__email = email
        self.__events = events
        # example events in self.__events
        # self.__events = {
        #   'MM-DD': [event1, event2, event3]
        # }


    def add_event(self, event):
        self.__events[event.date].append(event)
