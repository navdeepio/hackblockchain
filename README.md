# Hackblockchain

A crypto job board written in python and bulma

####Endpoints

`GET` `/user/login`

Return the login page

`POST` `/user/login`

Logs in the user

`GET` `/user/:id`

Show user dashboard

`GET` `/user/new`

Signup page

`POST` `/user/new`

Create new user and log them in

`GET` `/job/:id`

Show the job

`POST` `/job/:id`

Create the job

`PUT` `/job/:id`

Update the job

`GET` `/job/search`

Search the jobs for keywords and return the search page

####Tech Stack

* Flask
* Jinja2
* Bulma
* PostgreSQL

####License

GPL v 3.0