#!/bin/env python

from flask import Flask, render_template, redirect, url_for, flash, request
from dotenv import load_dotenv
import os
from flask_login import LoginManager, login_required, logout_user, \
    login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, CreateJobForm, JobSearchForm, \
    ForgotEmailForm, PasswordResetForm
from flask_sqlalchemy import SQLAlchemy

if os.getenv('FLASK_ENV') == 'development':
    load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '<o92_4$lor1123_0t'
db = SQLAlchemy(app)

from models import User, Job

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'


# login manager callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# homepage
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        jobs = Job.query.limit(5).all()
        return render_template('index.html', ads=jobs)


# maybe do the 'next' thing here
# login user
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
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
        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            flash('User already exists.')
            return redirect(url_for('create_user'))
        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    # form did not validate
    return render_template('login/sign-up.html', form=form)


# show user dashboard
@app.route('/user/dashboard', methods=['GET'])
@login_required
def dashboard():
    jobs = current_user.jobs
    email = current_user.email
    return render_template('user/dashboard.html', ads=jobs, email=email)


# Get an ad
@app.route('/job/<int:job_id>', methods=['GET'])
def show_job(job_id):
    ''' finds the particular job
     and returns it in its own page
     or edit the job
    '''
    job = Job.query.get(job_id)
    return render_template('ad/job_detailed.html', job=job)


# TODO: testing
# update an ad
@app.route('/job/edit/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    # fetch the job and do
    job = Job.query.get(job_id)
    form = CreateJobForm(obj=job)
    if form.validate_on_submit():
        flash('Job updated successfully')
        return redirect(url_for('dashboard'))
    return render_template('ad/new.html', form=form, job=job)


# create a job
@app.route('/job/new', methods=['GET', 'POST'])
@login_required
def job_form_create():
    '''
    returns the create ad form or
    creates the ad
    '''
    form = CreateJobForm()
    if form.validate_on_submit():
        user_id = current_user.id
        title = form.title.data
        job_location = form.job_location.data
        job_type = form.job_type.data
        job_description = form.job_description.data
        link_to_apply = form.link_to_apply.data
        company_name = form.company_name.data
        company_website = form.company_website.data
        job = Job(user_id=user_id, title=title, job_location=job_location,
                  job_type=job_type,
                  job_description=job_description,
                  link_to_apply=link_to_apply,
                  company_name=company_name,
                  company_website=company_website)
        db.session.add(job)
        db.session.commit()
        flash('Ad created successfully.')
        return redirect(url_for('dashboard'))
    return render_template('ad/new.html', form=form)


# TODO
# search through the ads
@app.route('/job/search', methods=['GET'])
def job_search():
    try:
        q = request.args.get('q')
    except KeyError:
        form = JobSearchForm()
        return render_template('ad/search.html', form=form)
    if q:
        jobs = Job.query.filter()
        return render_template('ad/search.html', jobs=jobs)
    else:
        form = JobSearchForm()
        return render_template('ad/search.html', form=form)


# delete ad
@app.route('/job/delete/<int:job_id>', methods=['GET'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if job.user.id == current_user.id:
        db.session.remove(job)
        db.session.commit()
        flash('Job delete successful.')
        return redirect(url_for('dashboard.html'))
    else:
        return render_template('401.html')


# forgot password
@app.route('/user/forgot', methods=['GET', 'POST'])
def forgot():
    message = '''If your email address exists in our database, an email containing
    password reset instructions has been sent to it.'''
    form = ForgotEmailForm()
    if form.validate_on_submit():
        # send email
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            # email found, send email
            pass
        return render_template('message.html', message=message)
    return render_template('login/forgot.html', form=form)


# TODO
# user password reset form
@app.route('/user/resetpassword', methods=['GET', 'POST'])
def reset_password():
    try:
        id = request.args.get('id')
        token = request.args.get('token')
    except KeyError:
        # page not found
        return render_template('404.html')
    user = User.query.get(id)
    return render_template('user/password_reset_success.html', user=user,
                           token=token)


@app.route('/user/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=os.getenv('PORT'))
