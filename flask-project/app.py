#!/usr/local/bin/python3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import LoginForm, ReminderEventForm, RegisterForm, CelebrityEventForm, EventEditForm, EventFilterForm, PasswordChangeForm
from flask_login import login_user, logout_user, login_required, current_user
from models import db, loginManager, UserModel, EventModel
from datetime import datetime
import requests
import json

# Create a new Flask application instance
app = Flask(__name__)
app.secret_key="secret"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthday.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize the login manager
loginManager.init_app(app)

def addUser(email, username, password):
    user = UserModel()
    user.setPassword(password)
    user.email = email
    user.username = username
    db.session.add(user)
    db.session.commit()

# Handler for bad requests
@loginManager.unauthorized_handler
def authHandler():
    form=LoginForm()
    flash('Please login to access this page', 'alert-danger')
    return render_template('login.html',form=form)


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
            flash('Please enter a valid email and password', 'alert-danger')
            return render_template('login.html',form=form)
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Please enter a valid email', 'alert-danger')
            return render_template('login.html',form=form)
        if not user.checkPassword(form.password.data):
            flash('Please enter a valid password', 'alert-danger')
            return render_template('login.html',form=form)
        login_user(user)
        session['email'] = form.email.data
        return redirect(url_for('reminders', order_by_date=0))
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
        logged_in = True
        user_name = current_user.username
    form=RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            if form.password.data != form.confirmPassword.data:
                flash('Passwords do not match', 'alert-danger')
            else:
                flash('Something went wrong in registration', 'alert-danger')
            return render_template('register.html',form=form)
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is None:
            if form.password.data == form.confirmPassword.data:
                addUser(form.email.data, form.username.data, form.password.data)
                flash('Registration successful', 'alert-success')
                session['email'] = form.email.data
                user = UserModel.query.filter_by(email=form.email.data).first()
                login_user(user)
                return redirect(url_for('reminders', order_by_date=0))
            else:
                flash('Passwords do not match', 'alert-danger')
                return render_template('register.html',form=form)
        else:
            flash('Email already registered', 'alert-danger')
            return render_template('register.html',form=form)    
    return render_template('register.html',form=form, logged_in=logged_in, user_name=user_name)


@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    logged_in = False
    user_name = ""
    if current_user.is_authenticated:
        logged_in = True
        user_name = current_user.username
    eventForm = ReminderEventForm()
    celebForm = CelebrityEventForm()
    if eventForm.validate_on_submit():
        event = EventModel()
        event.event_title = request.form['title']
        event.event_date = convert_date_to_julian(request.form['date'])
        event.user_owner = session.get('email')
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('reminders', order_by_date=0)) 
    if celebForm.validate_on_submit():
        event = EventModel()
        event.event_title = request.form['title']
        celeb_bday = get_celebrity_dob(event.event_title)
        if celeb_bday is None:
            flash('The birthday of the name you entered is not available.', 'alert-danger')
            return redirect(url_for('add_event'))
        event.event_date = convert_date_to_julian(celeb_bday)
        event.user_owner = session.get('email')
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('reminders', order_by_date=0))
    return render_template('add_event.html', eventForm=eventForm, celebForm=celebForm, logged_in=logged_in, user_name=user_name)


@app.route('/update_event/<int:event_id>', methods=["GET", "POST"])
def update_event(event_id):
    logged_in = False
    user_name = ""
    if current_user.is_authenticated:
        logged_in = True
        user_name = current_user.username
    event = EventModel.query.get(event_id)
    eventForm = ReminderEventForm(obj=event)
    if eventForm.validate_on_submit():
        event.event_title = request.form['title']
        event.event_date = convert_date_to_julian(request.form['date'])
        db.session.commit()
        return redirect(url_for('reminders', order_by_date=0))
    return render_template('update_event.html',  event=event, eventForm=eventForm, logged_in=logged_in, user_name=user_name)


@app.route('/delete_event/<int:event_id>', methods=["GET", "POST"])
def delete_event(event_id):
    event = EventModel.query.get(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('reminders', order_by_date=1))


def convert_date_to_julian(date_string):
    date_format = "%Y-%m-%d"
    date = datetime.strptime(date_string, date_format)
    # The large number is the offset to equal the noon of the entered date
    julian_day = date.toordinal() + 1721425
    return julian_day


def convert_date_from_julian(julian_date):
        date = datetime.fromordinal(julian_date - 1721425)
        month = date.month
        day = date.day
        # If we want to include year
        # year = date.year
        date_str = f"{month} / {day}"
        return date_str


@app.route('/reminders/<int:order_by_date>', methods=["GET", "POST"])
def reminders(order_by_date=0):
    eventFilterForm = EventFilterForm()
    logged_in = False
    user_name = ""
    if current_user.is_authenticated:
        logged_in = True
        user_name = current_user.username
    events = None
    # Check if there are any reminders in the database.
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
    return render_template('reminders.html', eventFilterForm=eventFilterForm, events=events, logged_in=logged_in, user_name=user_name)


def get_celebrity_dob(celebrity_name):
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
        flash('A connection error occurred.', 'alert-danger')
    except Exception as e:
        flash('An error occurred.', 'alert-danger')
    if not data:
        return None
    try:
        dob_str = data[0]['birthday']
        date_format = "%Y-%m-%d"
        date_object = datetime.strptime(dob_str, date_format)
        current_year = datetime.now().year
        date_object = date_object.replace(year=current_year)
        dob_str = date_object.strftime(date_format)
    # if a celebrity does not have a birthday listed in the API
    except KeyError:
        return None
    return dob_str
    
    
@app.route('/change_password', methods=["GET", "POST"])
def change_password():
    passwordChangeForm = PasswordChangeForm()
    if current_user.is_authenticated:
        logged_in = True
        user_name = current_user.username
        user = UserModel.query.filter_by(username=user_name).first()
    if passwordChangeForm.validate_on_submit() and logged_in:
        new_password = request.form['newPassword']
        user.setPassword(new_password)
        db.session.commit()
        return redirect(url_for('reminders', order_by_date=0))

    return render_template('change_password.html', passwordChangeForm=passwordChangeForm, logged_in=logged_in, user_name=user_name)
        

if __name__ == '__main__':
    # The host is set to '0.0.0.0' to make the app accessible from any IP address.
    # The default port is 5000.
    app.run(host='0.0.0.0', debug='true', port=5000)
