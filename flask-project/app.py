#!/usr/local/bin/python3
# Import the necessary modules

from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import LoginForm, ReminderEventForm, RegisterForm, CelebrityEventForm, EventEditForm, EventFilterForm
from flask_login import login_user, logout_user, login_required, current_user
from models import db, loginManager, UserModel, EventModel
# from event import Event
from datetime import datetime
import requests
import json


# Create a new Flask application instance
app = Flask(__name__)
app.secret_key="secret"

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthday.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize the database
db.init_app(app)
with app.app_context():
    db.create_all()

#initialize the login manager
loginManager.init_app(app)

# #testing event list
# my_events = []

def addUser(email, username, password):
    user = UserModel()
    user.setPassword(password)
    user.email = email
    user.username = username
    db.session.add(user)
    db.session.commit()

#handler for bad requests
@loginManager.unauthorized_handler
def authHandler():
    form=LoginForm()
    flash('Please login to access this page')
    return render_template('login.html',form=form)

# # some setup code because we don't have a registration page or database
# @app.before_first_request
# def create_table():
#     db.create_all()
#     user = UserModel.query.filter_by(email = 'xil1314@uw.edu' ).first()
#     if user is None:
#         addUser("xil1314@uw.edu","506506")
#     else:
#         logout_user()


@app.route('/')
def home():
    logged_in = False
    user_name = ""
    if current_user.is_authenticated:
        logged_in = True  # Update this based on user authentication status
        user_name = current_user.username
    # This function will be called when someone accesses the root URL
    return render_template('home.html', logged_in=logged_in, user_name=user_name)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Please enter a valid email and password')
            return render_template('login.html',form=form)
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Please enter a valid email')
            return render_template('login.html',form=form)
        if not user.checkPassword(form.password.data):
            flash('Please enter a valid password')
            return render_template('login.html',form=form)
        login_user(user)
        session['email'] = form.email.data
        # print(str(session.get('email')))
        return redirect(url_for('reminders'))
    return render_template("login.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/register', methods=["GET", "POST"])
def register():
    logged_in = False
    user_name = ""
    if current_user.is_authenticated:
        logged_in = True  # Update this based on user authentication status
        user_name = current_user.username
    form=RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            if form.password.data != form.confirmPassword.data:
                flash('Passwords do not match')
            else:
                flash('Something went wrong in registration')
            return render_template('register.html',form=form)
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is None:
            if form.password.data == form.confirmPassword.data:
                addUser(form.email.data, form.username.data, form.password.data)  # Need username validation?
                flash('Registration successful')
                session['email'] = form.email.data
                user = UserModel.query.filter_by(email=form.email.data).first()
                login_user(user)
                return redirect(url_for('reminders'))  # may need to go back to 'login' if still buggy
            else:
                flash('Passwords do not match')
                return render_template('register.html',form=form)
        else:
            flash('Email already registered')
            return render_template('register.html',form=form)    
    return render_template('register.html',form=form, logged_in=logged_in, user_name=user_name)

@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    logged_in = False
    user_name = ""
    if current_user.is_authenticated:
        logged_in = True  # Update this based on user authentication status
        user_name = current_user.username
    eventForm = ReminderEventForm()
    celebForm = CelebrityEventForm()
    if eventForm.validate_on_submit():
        # data collected from form to be added to db
        event = EventModel()
        event.event_title = request.form['title']
        event.event_date = convert_date_to_julian(request.form['date'])
        event.user_owner = session.get('email')  # Might be wrong (would this be easier if we had user_id in db instead of email being primary key?)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('reminders')) 
    if celebForm.validate_on_submit():
        # call api
        event = EventModel()
        event.event_title = request.form['title']
        celeb_bday = get_celebrity_dob(event.event_title)
        if celeb_bday is None:
            flash('The birthday of the name you entered is not available.')
            return redirect(url_for('add_event'))
        event.event_date = convert_date_to_julian(celeb_bday)
        event.user_owner = session.get('email')
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('reminders'))
        # if birthday not found, flash an error

    return render_template('add_event.html', eventForm=eventForm, celebForm=celebForm, logged_in=logged_in, user_name=user_name)


@app.route('/update_event/<int:event_id>', methods=["GET", "POST"])
def update_event(event_id):
    logged_in = False
    user_name = ""
    if current_user.is_authenticated:
        logged_in = True  # Update this based on user authentication status
        user_name = current_user.username
    event = EventModel.query.get(event_id)
    eventForm = ReminderEventForm(obj=event)

    if eventForm.validate_on_submit():
        # Update event details from the form
        event.event_title = request.form['title']
        event.event_date = convert_date_to_julian(request.form['date'])
        db.session.commit()
        return redirect(url_for('reminders'))

    return render_template('update_event.html',  event=event, eventForm=eventForm, logged_in=logged_in, user_name=user_name)

@app.route('/delete_event/<int:event_id>', methods=["GET", "POST"])
def delete_event(event_id):
    event = EventModel.query.get(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('reminders'))


# def get_events():
#     # will grab event data from db and create Event class objects for each event
#     # Event(date, title)
#     # event_list = []
#     # grab julian date and event name from db for each event tied to user
#     # add to list
#     # sort list and return
#     global my_events
#     my_events.sort()
#     return my_events

def convert_date_to_julian(date_string):
    date_format = "%Y-%m-%d"
    date = datetime.strptime(date_string, date_format)
    #other way is to use jdcal but couldn't get the import module working
    # the large number is the offset to equal the noon of the entered date
    julian_day = date.toordinal() + 1721425
    return julian_day

def convert_date_from_julian(julian_date):
        date = datetime.fromordinal(julian_date - 1721425)
        # date = datetime.fromordinal(int(julian_date) - 1721425)
        month = date.month
        day = date.day
        # if we want to include year
        # year = date.year
        date_str = f"{month} / {day}"
        return date_str

# @app.route('/reminders', methods=["GET", "POST"])
# def reminders():
#     # global my_events
#     events = db.session.query(EventModel).join(UserModel).filter(EventModel.user_owner==session.get('email')).all()
#     for event in events:
#         event.event_date = convert_date_from_julian(event.event_date)
#     return render_template('reminders.html', events=events)

@app.route('/reminders', methods=["GET", "POST"])
def reminders():
    eventFilterForm = EventFilterForm()
    logged_in = False
    user_name = ""
    if current_user.is_authenticated:
        logged_in = True  # Update this based on user authentication status
        user_name = current_user.username
    events = None
    # Check if there are any reminders in the database. (Check edge case if user is not logged in and goes to this page. Does this cause an error?)
    # events = EventModel.query.all()
    if current_user.is_authenticated:
        events = EventModel.query.filter_by(user_owner=current_user.email)

    # Format dates to be displayed properly in table
    for event in events:
        event.event_date = convert_date_from_julian(event.event_date)

    # Check if the user has searched for an event by title
    if eventFilterForm.validate_on_submit():
        filtered_events = []
        # events = EventModel.query.all()
        for event in events:
            if request.form['query'].lower() in str(event.event_title).lower():  # compare event title to only what the user has typed?
                filtered_events.append(event)
        return render_template('reminders.html', eventFilterForm=eventFilterForm, events=filtered_events, logged_in=logged_in, user_name=user_name)

    # return render_template('reminders.html', events=get_events())
    return render_template('reminders.html', eventFilterForm=eventFilterForm, events=events, logged_in=logged_in, user_name=user_name)


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
    try:
        # Make the API request
        response = requests.get(api_url, headers=headers, params=params)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        # Parse the response JSON
        data = response.json()
    except requests.exceptions.HTTPError as e:
        flash('A connection error occurred.')
    except Exception as e:
        flash('An error occurred.')
    if not data:
        return None
    # Extract and parse the date of birth
    # dob_str = str(data[0]['birthday'])
    dob_str = data[0]['birthday']
    # dob_datetime = datetime.strptime(dob_str, "%Y-%m-%d")
    return dob_str

# @app.route('/edit-event/<event_repr>', methods=["GET", "POST"])
# def edit_event(event_repr):
#     eventEditForm = EventEditForm()
#     event = EventModel.query.filter_by(event_id=event_repr).first()
#     event_title = event.event_title
#     event_display_date = convert_date_from_julian(event.event_date)
#     # event = id
#     return render_template('edit_event.html', eventEditForm=eventEditForm, 
#                            event=event, event_title=event_title, event_display_date=event_display_date)



# Run the application if this script is being run directly
if __name__ == '__main__':
    # The host is set to '0.0.0.0' to make the app accessible from any IP address.
    # The default port is 5000.
    app.run(host='0.0.0.0', debug='true', port=5000)
