# Insurance app

## Local development setup

### 1. Create the virtual environment and install the dependencies:

$ pipenv install --dev

### 2. Start the development postgresql database

$ docker-compose up

Notes: it runs on port 5432. The data is stored in .postgres_data.

### 3. Populate the database:

$ python manage.py migrate

### 4. Add a super user:

$ python manage.py createsuperuser --email [email] --username [username]

### 5. Run flake8 + tests + coverage report:

$ tox
