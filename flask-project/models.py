from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()
loginManager=LoginManager()

##CREATE TABLE
class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)
    events = db.relationship('EventModel', backref='user_model')
    
    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)
    
    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)
    
    def __repr__(self):
        return f'<User "{self.username}"'
    
class EventModel(UserMixin, db.Model):
    event_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    event_title = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.Integer, nullable=False)
    # user_owner = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    user_owner = db.Column(db.String(50), db.ForeignKey('user_model.email'), nullable=False)


    def __repr__(self):
        return f'<Event "{self.event_title}"'

@loginManager.user_loader
def loadUser(id):
    return UserModel.query.get(int(id))

# ##################################
# ###################################
# # Tom's code below (from get_and_sort_events.py in the "tom-dev" branch)
# #!/usr/bin/env python3
# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.orm import sessionmaker, relationship, DeclarativeMeta
# from sqlalchemy.orm import declarative_base
# from datetime import datetime, timedelta

# # Define base model for SQLAlchemy
# Base: DeclarativeMeta = declarative_base()


# # Define User model
# class User(Base):
#     __tablename__ = 'users'
#     user_email = Column(String, primary_key=True)
#     user_name = Column(String)
#     user_password = Column(String)
#     events = relationship("Event", back_populates='user')


# # Define Event model
# class Event(Base):
#     __tablename__ = 'events'
#     id = Column(Integer, primary_key=True)  # This line adds an auto-incrementing primary key
#     event_title = Column(String)
#     user_email = Column(String, ForeignKey('users.user_email'))
#     date_of_event = Column(Integer)  # Assuming date_of_event is still Julian day
#     user = relationship("User", back_populates='events')


# def ordinal(n):
#     return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))

# def get_events(user_email, session):
#     """
#     Fetches events for the given user and sorts them from earliest to latest.

#     Args:
#         user_email (str): Email address of the user.
#         session (sqlalchemy.orm.session.Session): SQLAlchemy Session object.

#     Returns:
#         None. Prints the events directly. Can be modified to return or process events as needed.
#     """
#     # Get the current year
#     current_year = datetime.now().year

#     # Fetch the user using the provided email
#     user = session.query(User).filter_by(user_email=user_email).first()
#     if user:
#         # If user is found, select events from the current day to 180 days in the future
#         events = session.query(Event).filter_by(user=user).filter(
#             Event.date_of_event.between(datetime.now().toordinal() - datetime(current_year, 1, 1).toordinal() + 1,
#                                         datetime.now().toordinal() - datetime(current_year, 1,
#                                                                               1).toordinal() + 180)).all()
#         # Sort the events by date and event title
#         sorted_events = sorted(events, key=lambda event: (event.date_of_event, event.event_title))
#         # Print each event; this can be replaced with other processing or return statements as needed
#         for event in sorted_events:
#             # Convert the Julian day to a datetime object
#             event_date = datetime(current_year, 1, 1) + timedelta(days=event.date_of_event - 1)
#             # Format the datetime object in the specified format
#             formatted_date = event_date.strftime('%A, %B ') + ordinal(event_date.day)
#             print(f'Event: {event.event_title}, Date: {formatted_date}')
#     else:
#         print(f'No user found with email: {user_email}')