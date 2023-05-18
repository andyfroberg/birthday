from user_preferences import UserPreferences

class User:
    def __init__(self, username, email, events=[],
                 user_preferences=UserPreferences()):
        self.username = username
        self.email = email
        self.events = events
        # example events in self.__events
        # self.__events = {
        #   'MM-DD': [event1, event2, event3]
        # }
        # Should events be organized by date in the database instead of
        # in a data structure here?
        self.__preferences = user_preferences


    def add_event(self, event):
        # self.__events[event.date].append(event)
        self.events.append(event)

    def remove_event(self, event):
        # input validation
        for e in self.events:
            if e.id == event.id:
                self.events.remove(e)

    # @property
    # def events():
    #     return self.__events
    