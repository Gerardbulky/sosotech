from wtforms import (Form, StringField, TextAreaField, PasswordField,SubmitField,
                     validators,FormField,DateTimeField, ValidationError)
from wtforms.validators import ValidationError, DataRequired,Email,Length
from flask_wtf import FlaskForm


class UsersForm(FlaskForm):
    fullname = StringField('Full names ', [validators.DataRequired()])
    email = StringField('Email address ', [validators.Email(), validators.DataRequired(),Email("This field requires a valid email address"),Length(max=120)])
    phone = StringField('Phone number ', [validators.DataRequired()])
    city_country = StringField('City & Country ', [validators.DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('', [validators.Email(), validators.DataRequired()])
    password = PasswordField('', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('', [validators.DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('', [validators.Email(), validators.DataRequired()])
    password = PasswordField('', [validators.DataRequired()])
    submit = SubmitField('Submit')