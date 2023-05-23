from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime

def validate_date(form, field):
    try:
        datetime.strptime(field.data, '%m-%d-%Y')
    except ValueError:
        raise ValidationError('Invalid date. Please enter a valid calendar date in the format MM-DD-YYYY.')

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=50)])

class NameAndDateForm(FlaskForm):
    firstName = StringField('firstName', validators=[DataRequired(), Length(min=1, max=50)])
    lastName = StringField('lastName', validators=[DataRequired(), Length(min=1, max=50)])
    date = DateField('date', format='%m-%d-%Y', validators=[DataRequired(), validate_date])

class DescriptionForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1, max=50)])
    description = TextAreaField('description', validators=[DataRequired(), Length(min=1, max=500)])
    date = DateField('date', format='%m-%d-%Y', validators=[DataRequired(), validate_date])
