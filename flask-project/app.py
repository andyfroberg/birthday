#!/usr/local/bin/python3
# Import the necessary modules

from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import LoginForm, NameAndDateForm, DescriptionForm
from flask_login import login_user, logout_user, login_required, current_user
from models import db, loginManager, UserModel
from event import NameAndDateEvent, DescriptionEvent

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
    user = UserModel.query.filter_by(email = 'lhhung@uw.edu' ).first()
    if user is None:
        addUser("lhhung@uw.edu","qwerty")
    else:
        logout_user()

# Define a route for the root URL ("/") that returns "Hello World"
@app.route('/home')
def birthdayReminder():
    # This function will be called when someone accesses the root URL
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Please enter a valid email and password')
            return render_template('login.html',form=form)
        user = UserModel.query.filter_by(email = form.email.data).first()
        if user is None:
            flash('Please enter a valid email')
            return render_template('login.html',form=form)
        if not user.checkPassword(form.password.data):
            flash('Please enter a valid password')
            return render_template('login.html',form=form)
        login_user(user)
        session['email'] = form.email.data
        return redirect(url_for('reminder.html'))
    # This function will be called when someone accesses the root URL
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    form=LoginForm()
    session.pop('username', None)
    # This function will be called when someone accesses the root URL
    return render_template('login.html', form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Create cursor
        cursor = connection.cursor()
        # Get the form data
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")
        # Check if a username was entered
        if not username:
            return render_template("register.html", error_message="Missing username. ")
        # Evaluate if the user does already exist
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        if row:
            return render_template("register.html", error_message="Username already exists. ")
        # Check if a password was entered
        if not password:
            return render_template("register.html", error_message="Missing password. ")
        # Check if a password confirmation was entered
        if not password_confirmation:
            return render_template("register.html", error_message="Missing password confirmation. ")
        # Check if password and password confirmation are equal
        if password != password_confirmation:
            return render_template("register.html", error_message="Passwords do not match. ")
        # Add user to database
        user = "INSERT INTO users (username, hash) VALUES(%s, %s)"
        data = (username, generate_password_hash(password))
        cursor.execute(user, data)
        connection.commit()
        # Close cursor
        cursor.close()
        return redirect("/")
    # This function will be called when someone accesses the root URL
    return render_template('register.html')

@app.route('/add_birthday', methods=["GET", "POST"])
def add_birthday():
    birthdayForm = NameAndDateForm()
    global my_events
    if birthdayForm.validate_on_submit():
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        date = request.form['date']
        full_name = f"{firstName} {lastName}"
        new_birthday = NameAndDateEventEvent(full_name, date)
        my_events.append(new_birthday)
        # add birthday to database
        return redirect(url_for('reminders'))
    # will have to get data entered by user and store into db
    return render_template('add_birthday.html', birthdayForm=birthdayForm)

def get_events():
    # will grab event data from db and create Event class objects
    # and return the list of them to be used in reminders to display events
    pass

@app.route('/reminders', methods=["GET", "POST"])
def reminders():
    global my_events
    return render_template('reminders.html', events=my_events)

# Run the application if this script is being run directly
if __name__ == '__main__':
    # The host is set to '0.0.0.0' to make the app accessible from any IP address.
    # The default port is 5000.
    app.run(host='0.0.0.0', debug='true', port=5000)
