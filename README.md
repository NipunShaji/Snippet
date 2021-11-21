# Snippet

Snippet is a tets project, which exposes a buch of API's to create, update, retrive and delete Snippets.
It also supports adding tags to snippets


## Set Up
* Clone the repo
* Setup a python virtual env and install the requirements from `requirements.txt` file
* DB already intialized to initial point, no need to run migrations
* Create super user `python manage.py createsuperuser`
* Run project `python manage.py runserver`
* Access admin from `http://localhost:8000/admin`


## Requirements

* Python 3.8
* Django
* Django Restframework
* Restframework SimpleJWT


## API Spec

### Auth
JWT
### Postman Collection
`https://www.getpostman.com/collections/f6db1f43703291f0127f`
