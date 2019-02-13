#! /bin/env python

from flask import Flask, render_template, redirect, url_for, flash, request
from dotenv import load_dotenv
import os
from flask_login import LoginManager, login_required, logout_user, \
    login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, CreateJobForm
from models import db, User, Job

if os.getenv('FLASK_ENV') == 'development':
    load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '<o92_4$lor1123_0t'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


# login manager callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email/password combination.')
            return redirect(url_for('user_login'))
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
    return render_template('ad/index.html', job=job)


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
    return render_template('ad/new.html', form=form, job=job)


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


# TODO
# search through the ads
@app.route('/job/search')
def job_search():
    q = None
    try:
        q = request.args.get('q')
    except KeyError:
        pass
    if q:
        return render_template('')
    return 'done'


# reset user password
@app.route('/user/resetpassword', methods=['GET', 'POST'])
def reset_password():
    id = None
    token = None
    try:
        id = request.args.get('id')
        token = request.args.get('token')
    except KeyError:
        # return 404
        pass

    if id and token:
        # both were present, carry out the verification here
        return 'verified'

    return 'pass'


# TODO
# forgot password
@app.route('/user/forgot', methods=['GET'])
def forgot():
    return render_template('user/forgot.html')


@login_required
@app.route('/user/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=os.getenv('PORT'))
