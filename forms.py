from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField


class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    # add remember me later


class RegistrationForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')


class CreateJobForm(FlaskForm):
    title = StringField('job_title')
    location = StringField('job_location')
    job_type = StringField('job_type') # have to define enum for this
    job_description = TextAreaField('job_description')
    link_to_apply = StringField('link_to_apply') # url?
    company_name = StringField('company_name')
    company_location = StringField('company_location')
    company_website = StringField('company_website') # url?
