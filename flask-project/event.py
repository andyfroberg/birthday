import datetime

class Event:
    
    def __init__(self, date, event_title):
        self.__julian_date = date
        self.date = self.convert_date_from_julian(self.__julian_date)
        self.event_title = event_title
    
    def __repr__(self):
        ret_str = ""
        ret_str += f"{self.__event_title}\n"
        ret_str += f"{self.__date}"
        return ret_str
    
    def __lt__(self, other):
        return self.julian_date < other.julian_date

    @property
    def julian_date(self):
        return self.__julian_date

    #############################################
    # Moved this function into app.py since we are not
    # using event objects. (We are instead pulling events
    # from the db). If we want to keep it here, we could make
    # this a static method and call Event.convert_date_from_julian(j_date)
    # from app.py. (We could also add convert_date_to_julian() here 
    # if we did that.)
    def convert_date_from_julian(self, julian_date):
        date = datetime.datetime.fromordinal(julian_date - 1721425)
        month = date.month
        day = date.day
        # if we want to include year
        # year = date.year
        date_str = f"{month} / {day}"
        return date_str
     #############################################