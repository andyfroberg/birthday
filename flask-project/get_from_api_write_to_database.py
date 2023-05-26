#!/usr/bin/env python3
import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy declarative base class
Base = declarative_base()


# User class mapped to "users" table in the database
class User(Base):
    __tablename__ = "users"
    user_email = Column(String, primary_key=True)  # User's email as primary key
    user_name = Column(String)  # User's name
    user_password = Column(String)  # User's password
    events = relationship("Event", back_populates="user")  # Relationship to the Event class/table


# Event class mapped to "events" table in the database
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)  # Event's ID as primary key
    event_title = Column(String)  # Title of the event
    user_email = Column(String, ForeignKey("users.user_email"))  # Foreign key referencing User's email
    date_of_event = Column(Integer)  # Date of the event
    user = relationship("User", back_populates="events")  # Relationship to the User class/table


def get_celebrity_dob(celebrity_name):
    """
    Fetches the date of birth of a celebrity from an API.

    Args:
        celebrity_name: Name of the celebrity.

    Returns:
        dob_datetime: The date of birth of the celebrity as a datetime object, or None if not found.
    """
    # API endpoint URL
    api_url = "https://api.api-ninjas.com/v1/celebrity"
    # Parameters for the API request
    params = {'name': celebrity_name.lower().replace(' ', '_')}
    headers = {'X-Api-Key': '4enulfTgfsbrl/wW7JiaoQ==jLNpv26JHetz3tHp'}
    # Make the API request
    response = requests.get(api_url, headers=headers, params=params)
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()
    # Parse the response JSON
    data = response.json()
    if not data:
        print(f"{celebrity_name}'s birthday is not available.")
        return None
    # Extract and parse the date of birth
    dob_str = data[0]['birthday']
    dob_datetime = datetime.strptime(dob_str, "%Y-%m-%d")
    return dob_datetime


def format_dob(dob):
    """
    Formats a date of birth as a string.

    Args:
        dob: The date of birth as a datetime object.

    Returns:
        A string representing the formatted date of birth.
    """
    day = dob.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return dob.strftime('%A, %B') + f" {day}{suffix}"


def main():
    """
    Main function to run the program.
    It fetches the date of birth of a celebrity, formats it, and stores an event in the database.
    """
    # Prompt the user to enter a celebrity's name
    name = input("Enter the celebrity's name: ")
    # Fetch the celebrity's date of birth
    dob = get_celebrity_dob(name)
    if dob is None:
        return
    # Format the date of birth
    dob_str = format_dob(dob)
    print(f"{name}'s birthday is {dob_str}.")

    # Database setup
    # Establish connection to SQLite database
    # Currently using the TEST database. FOR FINAL,CHANGE TO 'Birthday_Reminder.db'
    engine = create_engine('sqlite:///TEST_Birthday_Reminder_2.db')
    Base.metadata.create_all(engine)  # Create tables in the database
    Session = sessionmaker(bind=engine)  # Create a Session class bound to this engine
    session = Session()  # Instantiate a Session

    # Prompt the user to enter their email
    user_email = input("Enter your email: ")
    # Prepare the event title and date
    event_title = f"{name}'s Birthday"
    date_of_event = dob.timetuple().tm_yday  # Day of year

    # Check if the event already exists in the database
    existing_event = session.query(Event).filter(Event.event_title == event_title,
                                                 Event.user_email == user_email,
                                                 Event.date_of_event == date_of_event).first()
    if existing_event is not None:
        print("Event already exists in the database.")
    else:
        # If the event doesn't exist, create a new event and add it to the database
        event = Event(event_title=event_title, user_email=user_email, date_of_event=date_of_event)
        session.add(event)  # Add the new event to the session
        session.commit()  # Commit the transaction
        print("Event added to the database.")


if __name__ == '__main__':
    main()
