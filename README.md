# Insurance app

## For the evaluators

### The deliverables (in this repo):

1. This README
2. Via e-mail
3. insurance/models.py and insurance/tests/test_models.py
4. er-diagram.png
5. Using django-rest-framework:
  * insurance/serializers.py
  * insurance/views.py
  * insurance/tests/test_api.py
6. Same as item 5
7. index.html (you need to click on an risk type to display the form)
8. Very basic implementation, not using Vue components. I added models for 
storing the risks, but the app isn't handling form submissions.
9. Via e-mail
10. quiz.py
11. Same as item 2?
12. Via e-mail

## Using the deployed app

### Adding a new risk type

Access the /api/risk_types/ endpoint.
There you can use the raw data tab to post a new risk type. One example of
valid risk type is provided in the `sample_risk_type.json` file in this repository.

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

## Deploying changes to AWS

### Updating the code

$ zappa update [env]

### Running migrations

$ zappa manage [env] migrate

## AWS Setup (for new deployments)

### 1. Update the zappa_settings.json file to point to the new lambda function.

### 2. Deploy the project to the new lambda function

$ zappa deploy [env]

### 2. Create a new RDS database

Go to https://console.aws.amazon.com/rds and create a new database.
Save the user, password and database name.

Go to the newly created database details page and save: 
VPC, VPC security groups, Subnets, Endpoint and Port

### 3. Go to the Lambda network settings and select the VPC and Subnets you saved on the previous step.

### 4. Add the Lambda environment variables RDS_DB_USER, RDS_DB_NAME, RDS_DB_PASSWORD, RDS_DB_HOST

### 5. Add Inbound rule to Security Group

Go to the database details page, click on the security group link. Select the Inbound tab.
Add a new rule: Type = Postgresql, Source = the db security group. 

### 6. Add network settings to zappa_settings

Update the SecurityGroupIds and SubnetIds settings.

### 7. Create db

$ zappa manage dev create_pg_db

### 8. Run migrations

$ zappa manage [env] migrate

### 9. Create super user

$ zappa manage dev create_admin_user
