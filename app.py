#! /bin/env python
from flask import Flask, render_template, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

if os.getenv('FLASK_ENV') == 'development':
    load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    jobs = db.relationship('Job', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, unique=True, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, unique=True, nullable=False,
                           default=datetime.utcnow)
    # create a hook to update updated_at every time this is saved


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    how_to_apply = db.Column(db.String(300), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # type of job, need an enum for that


# homepage
@app.route('/')
def index():
    return render_template('index.html')


# login user
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login/sign-in.html')
    elif request.method == 'POST':
        print('login the user')


# create user
@app.route('/user/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('login/sign-up.html')
    elif request.method == 'POST':
        print('have to create the user now')


# show user dashboard
@app.route('/user/<int:id>', methods=['GET'])
def show_edit_user():
    return render_template('dashboard.html')


# Get or update an ad
@app.route('/job/<int:id>', methods=['GET', 'PATCH'])
def show_edit_job():
    if (request.method == 'GET'):
        ''' finds the particular job
         and returns it in its own page
         or edit the job
        '''
        return render_template('job.html')
    elif (request.method == 'PATCH'):
        return 'patched the request'


# create a job
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
    else:
        return 'page not found'


# search through the ads
@app.route('/job/search')
def job_search():
    return 'done'


# reset user password
@app.route('/user/resetpassword')
def reset_password():
    return 'the job search page'


if __name__ == '__main__':
    app.run(port=os.getenv('PORT'))
