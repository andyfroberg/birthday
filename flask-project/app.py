#!/usr/local/bin/python3
# Import the necessary modules

from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import LoginForm, ReminderEventForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from models import db, loginManager, UserModel
from event import Event
import datetime


# Create a new Flask application instance
app = Flask(__name__)
app.secret_key="secret"

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize the database
db.init_app(app)

#initialize the login manager
loginManager.init_app(app)

#testing event list
my_events = []

def addUser(email, password):
    user = UserModel()
    user.setPassword(password)
    user.email=email
    db.session.add(user)
    db.session.commit()

#handler for bad requests
@loginManager.unauthorized_handler
def authHandler():
    form=LoginForm()
    flash('Please login to access this page')
    return render_template('login.html',form=form)

# some setup code because we don't have a registration page or database
@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = 'xil1314@uw.edu' ).first()
    if user is None:
        addUser("xil1314@uw.edu","506506")
    else:
        logout_user()


@app.route('/home')
def home():
    # This function will be called when someone accesses the root URL
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Please enter a valid email and password')
            return render_template('login.html',form=form)
        user = UserModel.query.filter_by(email=form.email.data ).first()
        if user is None:
            flash('Please enter a valid email')
            return render_template('login.html',form=form)
        if not user.checkPassword(form.password.data):
            flash('Please enter a valid password')
            return render_template('login.html',form=form)
        login_user(user)
        session['email'] = form.email.data
        return redirect(url_for('reminders'))
    return render_template("login.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    session.pop('email', None)
    # Currently no logout.html redirects to login page after logout, which I suppose is fine?
    return redirect(url_for('login'))

@app.route('/register', methods=["GET", "POST"])
def register():
    form=RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            if form.password.data != form.confirmPassword.data:
                flash('Passwords do not match')
            else:
                flash('Something went wrong in registration')
            return render_template('register.html',form=form)
        user = UserModel.query.filter_by(email = form.email.data ).first()
        if user is None:
            if form.password.data == form.confirmPassword.data:
                addUser(form.email.data, form.password.data)
                flash('Registration successful')
                return redirect(url_for('login'))
            else:
                flash('Passwords do not match')
                return render_template('register.html',form=form)
        else:
            flash('Email already registered')
            return render_template('register.html',form=form)    
    return render_template('register.html',form=form)

@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    eventForm = ReminderEventForm()
    global my_events
    if eventForm.validate_on_submit():
        # data collected from form to be added to db
        title = request.form['title']
        date = request.form['date']
        date = convert_date_to_julian(date)
        # mock event creation this will be done in get_events
        new_event = Event(date, title)
        my_events.append(new_event)
        return redirect(url_for('reminders'))
    return render_template('add_event.html', eventForm=eventForm)

def get_events():
    # will grab event data from db and create Event class objects for each event
    # Event(date, title)
    # event_list = []
    # grab julian date and event name from db for each event tied to user
    # add to list
    # sort list and return
    global my_events
    my_events.sort()
    return my_events

def convert_date_to_julian(date_string):
    date_format = "%Y-%m-%d"
    date = datetime.datetime.strptime(date_string, date_format)
    #other way is to use jdcal but couldn't get the import module working
    # the large number is the offset to equal the noon of the entered date
    julian_day = date.toordinal() + 1721425
    return julian_day

@app.route('/reminders', methods=["GET", "POST"])
def reminders():
    global my_events
    return render_template('reminders.html', events=get_events())

# Run the application if this script is being run directly
if __name__ == '__main__':
    # The host is set to '0.0.0.0' to make the app accessible from any IP address.
    # The default port is 5000.
    app.run(host='0.0.0.0', debug='true', port=5000)
