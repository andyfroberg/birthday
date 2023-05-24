from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=50)])


class RegisterForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=50)])
    confirmPassword = PasswordField('confirmPassword', validators=[DataRequired(), EqualTo('password'), Length(min=5, max=50)])


class NameAndDateForm(FlaskForm):
    firstName = StringField('firstName', validators=[DataRequired(), Length(min=1, max=50)])
    lastName = StringField('lastName', validators=[DataRequired(), Length(min=1, max=50)])
    date = DateField('date', format= '%Y-%m-%d', validators=[DataRequired()])

    

class DescriptionForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1, max=50)])
    description = TextAreaField('description', validators=[DataRequired(), Length(min=1, max=500)])
    date = DateField('date', format='%Y-%m-%d', validators=[DataRequired()])
