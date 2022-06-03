
I share my researches, studies and assignments for the course. 

You can visit Wiki page to see more details.

Code can be reached from master branch.

## Clone project files to your local machine
	git clone [https://github.com/arcanaktepe/swe5732021fall.git](https://github.com/iremacildi/SWE574-Group03.git)

## Create virtual environment
  > run python -m .env  <name_of your_virtualenv>
## Activate virtual environment
> ‘cd <name_of your_virtualenv>’, ‘cd Scripts’, ‘Activate’	with following order.
  
## Install Postgresql 14.1
## Install PgAdmin4
## Create Database
## Install requirements
> pip install -r requirements.txt
## Apply Migrations
> python manage.py make migrations
> python manage.py migrate
## Apply Actstream Migration
> set USE_JSONFIELD setting as False  
> run python manage.py migrate actstream 0001  
> set USE_JSONFIELD setting as True  
> run python manage.py migrate actstream
## Apply Notifications Migration
> run python manage.py migrate notifications
## Run server
> python manage.py runserver
