from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField, TextField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=2, max=25), DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign In')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    submit = SubmitField('Add')