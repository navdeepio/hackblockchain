# Hackblockchain

A crypto job board written in python and bulma

#### Endpoints

`GET` `/`

Home page

`GET` `/user/login`

Return the login page

`POST` `/user/login`

Logs in the user

`GET` `/user/new`

Signup page

`POST` `/user/new`

Create new user and log them in

`GET` `/user/dashboard`

Show user dashboard

`GET` `/user/forgot`

Show the forgot password page

`GET` `/user/resetpassword`

Reset the user password after verifying the token

`GET` `/job/:id`

Show ad page

`GET` `/job/:id/edit`

Show the edit ad page

`POST` `/job/:id/edit`

Update the ad

`GET` `/job/:id/delete`

Delete the ad

`GET` `/job/new`

Show the create ad form

`POST` `/job/new`

Create the ad

`GET` `/job/search`

Search the jobs for keywords and return the search page

#### Tech Stack

* Flask
* Jinja2
* Bulma
* PostgreSQL

#### License

GPL v3.0
