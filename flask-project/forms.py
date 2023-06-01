from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=50)])


class RegisterForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    username = StringField('username', validators=[DataRequired(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=50)])
    confirmPassword = PasswordField('confirmPassword', validators=[DataRequired(), EqualTo('password'), Length(min=5, max=50)])


class ReminderEventForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1, max=50)])
    date = DateField('date', format= '%Y-%m-%d', validators=[DataRequired()])

class CelebrityEventForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1, max=50)])

class EventEditForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1, max=50)])
    date = DateField('date', format= '%Y-%m-%d', validators=[DataRequired()])

class PasswordChangeForm(FlaskForm):
    newPassword = PasswordField('newPassword', validators=[DataRequired(), Length(min=5, max=50)])
    confirmNewPassword = PasswordField('confirmNewPassword', validators=[DataRequired(), EqualTo('newPassword'), Length(min=5, max=50)])