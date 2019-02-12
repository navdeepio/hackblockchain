#! /bin/env python

from flask import Flask, render_template, redirect, url_for, flash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from enum import Enum
from flask_login import LoginManager, UserMixin, login_required, logout_user, \
    login_user, current_user
from forms import LoginForm, RegistrationForm, CreateJobForm
from werkzeug.security import generate_password_hash, check_password_hash

if os.getenv('FLASK_ENV') == 'development':
    load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '<o92_4$lor1123_0t'
db = SQLAlchemy(app)

login_manager = LoginManager()
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
    jobs = current_user.jobs
    return render_template('user/dashboard.html', jobs=jobs)


# Get an ad
@app.route('/job/<int:job_id>', methods=['GET'])
def show_job(job_id):
    ''' finds the particular job
     and returns it in its own page
     or edit the job
    '''
    job = Job.query.get(job_id)
    return render_template('job/index.html', job=job)


# update an ad
@login_required
@app.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
def edit_job(job_id):
    # fetch the job and do
    job = Job.query.get(job_id)
    form = CreateJobForm()
    if form.validate_on_submit():
        flash('Job updated successfully')
        return redirect(url_for('dashboard'))
    return render_template('job/new.html', form=form, job=job)


# create a job
@login_required
@app.route('/job/new', methods=['GET', 'POST'])
def job_form_create():
    '''
    returns the create ad form or
    creates the ad
    '''
    form = CreateJobForm()
    if form.validate_on_submit():
        #
        flash('Created successfully.')
        return redirect(url_for('dashboard'))
    return render_template('job/new.html', form=form)


# search through the ads
@app.route('/job/search')
def job_search():
    '''
    work to be done here
    '''
    return 'done'


# reset user password
@app.route('/user/resetpassword', methods=['GET', 'POST'])
def reset_password():
    # get query params
    return 'reset password page'


# forgot password
@app.route('/user/forgot', methods=['GET'])
def forgot():
    return render_template('user/forgot.html')


@app.route('/user/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=os.getenv('PORT'))
