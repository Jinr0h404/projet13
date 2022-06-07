# projet13
final project of the OC python application dev OC training
is to present the activity and the profession of a person through a showcase site and to have access to an
administrative part to manage his activity as an osteopath through planning tools, creation of patient file
and consultation file
Application host on Heroku, visible at: [link to the web app](https://apposteo.herokuapp.com/)


## START
This project uses Python and Requests library. It is advisable to use
a virtual environment to avoid conflicts with other version of libraries.


## pre requirement
to start the webapp, you need:
* Python
* Git
* PostgreSql
* Requests library (auto install later with requirements)


## INSTALLATION

1. Download sources from github repository:
[link to github repo](https://github.com/Jinr0h404/Projet13.git)

You can dowload zip file or dowload with the url and Git:
- create new folder for Project, with Git in root of the folder
- Make git clone https://github.com/Jinr0h404/Projet13.git

2. If you don't have it: Install Python 3.9 and requirements file.
You will find the sources for Python here:
[link to sources](https://www.python.org/downloads/)

3. **Strongly advised:**
Install a virtual environment like Pipenv:
install with command: `pip install pipenv`
to use pipenv: 
in project folder, init virtual env with command: `pipenv shell`
when you are in your virtual environment you can install libraries from requirements
file with command: `pip install -r requirements.txt`


## CONFIGURATION
**Strongly advised:**
the configurations below relate to sending mail and database information. 
They are specific to your project and contain security information,
so it is recommended to put them in environment variables and not in clear in the settings.py file

**Before starting the application:**
1. the application manages the sending of mail through the contact form
This part is to be configured in the settings.py file according to your mail server:
**# EMAIL SETUP**
* `EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`
* `EMAIL_HOST = smtp server address, for example: 'smtp.gmail.com'`
* `EMAIL_HOST_USER = your smtp username, for example: 'name@gmail.com'`
* `EMAIL_HOST_PASSWORD = 'your password'`
* `EMAIL_PORT = the smtp port of your mail server, for example for gmail: 587`
* `EMAIL_USE_TLS = True`
* `DEFAULT_FROM_EMAIL = optional, matches the displayed sender name, for example: 'support team <noreply@myapp.com>'`

2. About the database:
- `'ENGINE': 'django.db.backends.postgresql',`
- `'NAME': the name of the database used`
- `'USER': the username having access to the database`
- `'PASSWORD': the user's password`
- `'HOST': the address of the database server, in our case: 'localhost'`
- `'PORT': the port of the database server, in the case of postgres by default '5432'`

3. Administrative management part:
To take advantage of this part you will need to create a superuser in order to log in to the administration
interface at the address http://127.0.0.1:8000/gestionosteo 
- `python manage.py createsuperuser`

4. edition of invoice in pdf tool:
Also fill in the columns of the price table in the database with the values you want for the price and the type
of consultation in order to take advantage of the invoice editing tool.
you can do this directly from your database, or by going through the django admin bdd interface at the address 
http://127.0.0.1:8000/gestionbdd or by loading the export of the project table with the command:
- `python manage.py loaddata price.json`

## Application

To start the application
* In the virtual env
* start the web server with command: `python manage.py runserver`


## Result

Server web is running.
You could go on http://127.0.0.1:8000/ to try your app
and on http://127.0.0.1:8000/gestionosteo for the administration part of the app 


## PROJECT

made with:

* Django==3.2.9
* gunicorn==20.1.0
* psycopg2==2.9.2
* pytest==6.2.5
* pytest-cov==3.0.0
* pytest-django==4.4.0
* pytest-mock==3.6.1
* requests==2.26.0
* selenium==4.1.0
* whitenoise==5.3.0
* PostgreSql
* reportlab==3.6.9
* bootstrap template from https://startbootstrap.com/ under MIT license

## Contributor & Author

Ewen Jeannenot & bootstrap template from https://startbootstrap.com/ Copyright (c) 2013-2021 Start Bootstrap LLC