#!/usr/bin/env python3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeMeta
from sqlalchemy.orm import declarative_base
from typing import Type

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_email = Column(String, primary_key=True)
    user_name = Column(String)
    user_password = Column(String)
    events = relationship("Event", back_populates='user')


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)  # Added this line
    event_title = Column(String)
    user_email = Column(String, ForeignKey('users.user_email'))
    date_of_event = Column(String)  # Modified this line to be a String
    user = relationship("User", back_populates='events')


def main():
    """
    The main function that is the entry point of the script.
    It sets up the SQLite database and creates dummy users and events for testing.
    """
    engine = create_engine('sqlite:///Birthday_Reminder_sqlalchemy.db')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create dummy users
    users = [('Hong', 'lhhung@uw.edu', 'qwerty'),
             ('Sheehan', 'sheehan1025@gmail.com', 'STAXpassword1'),
             ('Tom', 'tjswanson314@gmail.com', 'STAXpassword2'),
             ('Andy', 'andy@email.com', 'STAXpassword3'),
             ('Xiying', 'xiying@email.com', 'STAXpassword4')
             ]

    # Define dummy events
    events = [
        ("Hong's TCSS 506 Class", 'lhhung@uw.edu', '2023-05-20'),
        ("Hong's TCSS 506 Class", 'lhhung@uw.edu', '2023-05-27'),
        ("Hong's TCSS 506 Class", 'lhhung@uw.edu', '2023-06-03'),
        ("Hong's TCSS 506 Project Due", 'lhhung@uw.edu', '2023-06-09'),
        ("Sheehan's Game", 'sheehan1025@gmail.com', '2023-06-15'),
        ("Sheehan's Project", 'sheehan1025@gmail.com', '2022-03-01'),
        ("Sheehan's Trip", 'sheehan1025@gmail.com', '2025-05-30'),
        ("Meredith's & Tom's Anniversary", 'tjswanson314@gmail.com', '2006-08-15'),
        ("Henry's Birthday", 'tjswanson314@gmail.com', '2010-10-09'),
        ("Meredith's Birthday", 'tjswanson314@gmail.com', '1978-08-31'),
        ("Tom's Birthday", 'tjswanson314@gmail.com', '1978-08-07'),
        ("Bennett's Birthday", 'tjswanson314@gmail.com', '2014-05-29'),
        ("Andy's Party", 'andy@email.com', '2023-07-08'),
        ("Andy's 1st Day on the Job", 'andy@email.com', '2024-01-01'),
        ("Andy's Other Party", 'andy@email.com', '2023-09-31'),
        ("Xiying's Graduation", 'xiying@email.com', '2023-09-24'),
        ("Candace's Graduation", 'xiying@email.com', '2023-09-24')
    ]

    # Insert users and their respective events into the tables
    for user in users:
        user_name, user_email, user_password = user
        new_user = User(user_name=user_name, user_email=user_email, user_password=user_password)
        session.add(new_user)

    session.commit()  # Commit here to make sure all users are in the database before adding events

    for event in events:
        event_title, user_email, date_of_event = event
        user = session.query(User).filter_by(user_email=user_email).first()
        if user is not None:
            new_event = Event(event_title=event_title, user_email=user_email, date_of_event=date_of_event)
            session.add(new_event)

    session.commit()


if __name__ == '__main__':
    main()
