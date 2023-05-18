#!/usr/local/bin/python3

from flask import Flask, render_template
from datetime import datetime
from user import User
from event import Event

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/events')
def events():
    user = User('andy', 'andy.froberg@gmail.com')
    user.add_event(Event('Mom bday', '05-12'))
    user.add_event(Event('dad bday', '08-13'))
    user.add_event(Event('sis bday', '08-15'))
    user.add_event(Event('bro bday', '08-03'))
    return render_template('events.html', user=user)

@app.route('/settings')
def settings():
    user = User('andy', 'andy.froberg@gmail.com')
    user.add_event(Event('Mom bday', '05-12'))
    user.add_event(Event('dad bday', '08-13'))
    user.add_event(Event('sis bday', '08-15'))
    user.add_event(Event('bro bday', '08-03'))
    return render_template('settings.html', user=user)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)