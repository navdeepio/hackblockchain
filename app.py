#! /bin/env python

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from enum import Enum
from flask_login import LoginManager, UserMixin, login_required, logout_user, \
    login_user
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

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


# login manager callback
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

    def __repr__(self):
        return '<User %r>' % self.email


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
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            redirect(url_for('dashboard'))
        else:
            flash('Invalid email/password combination.')
            redirect(url_for('user_login'))
    # have to add errors here
    return render_template('login/sign-in.html', form=form)


# create user
@app.route('/user/new', methods=['GET', 'POST'])
def create_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        # log in , user
        login_user(user)
        return redirect(url_for('dashboard'))
    # the dashboard should have a create job button
    # form did not validate
    return render_template('login/sign-up.html', form=form)


# show user dashboard
@login_required
@app.route('/user/dashboard', methods=['GET'])
def dashboard():
    return render_template('user/index.html')


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
