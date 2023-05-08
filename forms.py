from wtforms import (Form, StringField, TextAreaField, PasswordField,SubmitField,
                     validators,FormField,DateTimeField, ValidationError)
from wtforms.validators import ValidationError, DataRequired,Email,Length
from flask_wtf import FlaskForm


class UsersForm(FlaskForm):
    fullname = StringField('Full names ', [validators.DataRequired()])
    email = StringField('Email address ', [validators.Email(), validators.DataRequired(),Email("This field requires a valid email address"),Length(max=120)])
    phone = StringField('Phone number ', [validators.DataRequired()])
    address = StringField('Address ', [validators.DataRequired()])
    city_country = StringField('City & Country ', [validators.DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('', [validators.Email(), validators.DataRequired()])
    password = PasswordField('', [validators.DataRequired(), validators.EqualTo('confirms', message=' Both password must match! ')])
    confirms = PasswordField('', [validators.DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('', [validators.Email(), validators.DataRequired()])
    password = PasswordField('', [validators.DataRequired()])


class ContactForm(FlaskForm):
    name = StringField('', [validators.DataRequired()])
    email = StringField('', [validators.Email(), validators.DataRequired(),Email("This field requires a valid email address"),Length(max=120)])
    messages = TextAreaField('', [validators.DataRequired()])