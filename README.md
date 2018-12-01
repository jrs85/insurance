# Insurance app

### Local development

To create a virtual environment and install the dependencies:

$ pipenv install

To run flake8 + tests + coverage report:

$ tox

To instantiante the database:

$ python manage.py migrate

Add a super user:

$ python manage.py createsuperuser --email [email] --username [username]
