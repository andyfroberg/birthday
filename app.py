#!/usr/bin/python3

from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home(name=None):
    return render_template('index.html', name=name)

@app.route('/login')
def name(name=None):
    return render_template('login.html', name=name)

@app.route('/preferences')
def time(name=None):
    return render_template('preferences.html', name=name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)