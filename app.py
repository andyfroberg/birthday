from datetime import datetime

class App:
    def __init__(self):
        self.__users = []  # Get users from database
        self.__day_of_year = datetime.today().strftime('%m-%d')

    def register_user(self, user):
        self.__users.append(user)

    def check_events(self):
        for user in self.__users:
            for event in user.events:
                if event.date == self.__day_of_year:
                    self.notify_user(user, event)

    def notify_user(self, user, events):
        pass


if __name__ == "__main__":
    pass
    # a = App()
    # a.print_date()