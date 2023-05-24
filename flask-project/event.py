import datetime

class Event:
    
    def __init__(self, date, event_title, event_description=None):
        self.__date = self.convert_date_from_julian(date)
        self.__event_title = event_title
        self.__event_description = event_description
    
    def __repr__(self):
        ret_str = ""
        ret_str += f"{self.event_title}\n"
        if self.__event_description:
            ret_str += f"{self.__event_description}"
        ret_str += f"{self.__date}"
        return ret_str
    
    def convert_date_from_julian(self, julian_day):
        date = datetime.datetime.fromordinal(julian_day - 1721425)
        month = date.month
        day = date.day
        date_str = f"{month} / {day}"
        return date_str
