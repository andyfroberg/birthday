#!/usr/bin/env python3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeMeta
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta
from event import Event

# Define base model for SQLAlchemy
Base: DeclarativeMeta = declarative_base()


# Define User model
class User(Base):
    __tablename__ = 'users'
    user_email = Column(String, primary_key=True)
    user_name = Column(String)
    user_password = Column(String)
    events = relationship("Event", back_populates='user')


# Define Event model
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)  # This line adds an auto-incrementing primary key
    event_title = Column(String)
    user_email = Column(String, ForeignKey('users.user_email'))
    date_of_event = Column(Integer)  # Assuming date_of_event is still Julian day
    user = relationship("User", back_populates='events')


def ordinal(n):
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def get_events(user_email, session):
    """
    Fetches events for the given user and sorts them from earliest to latest.

    Args:
        user_email (str): Email address of the user.
        session (sqlalchemy.orm.session.Session): SQLAlchemy Session object.

    Returns:
        list : list of Event objects
    """
    # Get the current year
    current_year = datetime.now().year

    # Fetch the user using the provided email
    user = session.query(User).filter_by(user_email=user_email).first()
    if user:
        # If user is found, select events from the current day to 180 days in the future
        events = session.query(Event).filter_by(user=user).filter(
            Event.date_of_event.between(datetime.now().toordinal() - datetime(current_year, 1, 1).toordinal() + 1,
                                        datetime.now().toordinal() - datetime(current_year, 1,
                                                                              1).toordinal() + 180)).all()
        # Sort the events by date and event title
        sorted_events = sorted(events, key=lambda event: (event.date_of_event, event.event_title))
        # Print each event; this can be replaced with other processing or return statements as needed
        event_lst = []
        for event in sorted_events:
            # Convert the Julian day to a datetime object
            # event_date = datetime(current_year, 1, 1) + timedelta(days=event.date_of_event - 1)
            # Format the datetime object in the specified format
            # formatted_date = event_date.strftime('%A, %B ') + ordinal(event_date.day)
            # print(f'Event: {event.event_title}, Date: {formatted_date}')
            
            # creates a list of Event class objects to be returned for app.py to render on reminders.html
            # currently julian date conversion occurs at creation of Event object, but can be changed if needed
            even_lst.append(Event(event.date_of_event, event.event_title))
        return event_lst
    else:
        print(f'No user found with email: {user_email}')


def main():
    """
    The main function that is the entry point of the script.
    It sets up the SQLite database and fetches upcoming events for a specific user.
    """
    # Set up database engine and session
    engine = create_engine('sqlite:///Birthday_Reminder.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch all users' emails
    user_emails = session.query(User.user_email).all()

    # Fetch and print events for each user
    for email_tuple in user_emails:
        user_email = email_tuple[0]
        print(f'\nEvents for {user_email}:')
        get_events(user_email, session)


if __name__ == '__main__':
    main()
