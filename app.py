#! /bin/env python

from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from enum import Enum
from flask_login import LoginManager, UserMixin, login_required, logout_user
from forms import LoginForm, RegistrationForm

if os.getenv('FLASK_ENV') == 'development':
    load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'so92_4$lor1123sor'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'user_login'
login_manager.init_app(app)


# mandatory login manager callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Models begin


class JobType(Enum):
    contract = 'Contract'
    full_time = 'Full Time'
    part_time = 'Part Time'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    jobs = db.relationship('Job', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, unique=True, nullable=False,
                           default=datetime.utcnow)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    link_to_apply = db.Column(db.String(300), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_location = db.Column(db.String(100))
    company_name = db.Column(db.String(100), nullable=False)
    company_url = db.Column(db.String(300), nullable=False)
    job_type = db.Column(db.Enum(JobType), nullable=False)
    remote_ok = db.Column(db.Boolean, nullable=False, default=False)


# homepage
@app.route('/')
def index():
    return render_template('index.html')


# login user
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login/sign-in.html', form=form)
    elif request.method == 'POST':
        print('login the user')


# create user
@app.route('/user/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('login/sign-up.html', form=form)
    elif request.method == 'POST':
        print('have to create the user now')


# show user dashboard
@login_required
@app.route('/user/me', methods=['GET'])
def show_user():
    return render_template('dashboard.html')


# Get an ad
@login_required
@app.route('/job/<int:id>', methods=['GET'])
def show_job():
    ''' finds the particular job
     and returns it in its own page
     or edit the job
    '''
    return render_template('job.html')


# update an ad
@login_required
@app.route('/job/<int:id>', methods=['PATCH'])
def edit_job():
    return 'patched the request'


# create a job
@login_required
@app.route('/job/new', methods=['GET', 'POST'])
def job_form_create():
    '''
    returns the create ad form or
    creates the ad
    '''
    if request.method == 'GET':
        # do something
        return render_template('create_ad.html')
    elif request.method == 'POST':
        # do something else
        print('created the job')


# search through the ads
@app.route('/job/search')
def job_search():
    '''
    work to be done here
    '''
    return 'done'


# reset user password
@app.route('/user/resetpassword')
def reset_password():
    return 'reset password page'


@app.route('/user/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=os.getenv('PORT'))
