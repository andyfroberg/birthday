from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=50)])

class BirthdayForm(FlaskForm):
    firstName = StringField('firstName', validators=[DataRequired(), Length(min=1, max=50)])
    lastName = StringField('lastName', validators=[DataRequired(), Length(min=1, max=50)])