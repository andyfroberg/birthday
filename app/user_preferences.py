

class UserPreferences:
    def __init__(self, notification_week_of=True, notification_day_of=True):
        self.__notification_week_of = notification_week_of
        self.__notification_day_of = notification_day_of

    @property
    def notification_week_of(self):
        return self.__notification_week_of

    @notification_week_of.setter
    def notification_week_of(self, boolean):
        self.__notification_week_of = boolean

    @property
    def notification_day_of(self):
        return self.__notification_day_of

    @notification_day_of.setter
    def notification_day_of(self, boolean):
        self.__notification_day_of = boolean



