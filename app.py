#! /bin/env python
from flask import Flask, render_template, request
app = Flask(__name__)


# login user
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        print('login the user')


# create user
@app.route('/user/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('signup.html')
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
    app.run(debug=True, port=3000)
