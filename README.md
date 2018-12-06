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

