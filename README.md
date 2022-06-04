
### Bogazici University - Software Engineering, M.Sc.

## 2022 Spring Semester Software Engineering SWE574 Group 3 Project Repository

This repo will serve SWE574 course on 2022, Spring semester. 
We will present our researches, code, project details such as milestones, issues and the results.

Please check out our Wiki for further details.

## How to install Eventify?

To use this project, first clone the repo on your device using the command below:

```git init```

```git clone git clone https://github.com/iremacildi/SWE574-Group03.git```

## System Manual

Before starting, please make sure your local system has postgresql, docker and git.

- Create a virtual environment (arbitrary name for virtual env is “myvenv”)
- Go to project directory and in your IDE terminal please write: “source myvenv/bin/activate”
- Install Dependencies $ pip install -r requirements.txt
- Go to “.env” from main project directory through your IDE. 
- Update the inside of the document as follows.
```
 * DJANGO_SECRET_KEY= <your django secret key>
 * DJANGO_DEBUG=True
 * DJANGO_ALLOWED_HOSTS="127.0.0.1"
 * DB_ENGINE=django.db.backends.postgresql_psycopg2
 * DB_NAME=eventify
 * DB_USER=postgres
 * DB_PASSWORD=Pass1234
 * DB_HOST=127.0.0.1
 * DB_PORT=5432
 * CORS_ALLOWED_ORIGINS="http://localhost:3000 http://127.0.0.1:3000"
 ```
 - Update docker-compose.yml as follows

```
version: '3.8'
 
services:


           
  web:
   container_name: core_eventify
   build: .
   restart: always
   env_file: ./web/.env
   volumes:
     - .:/web
     - static_volume:/web/static
   depends_on:
     - db 

   ports:
     - 80:8000
  
  db:
    container_name: core_db
    image: postgres:14.1-alpine
    env_file:  ./web/.env
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
     - 5433:5432


volumes:
  static_volume:
  postgres_data:
  nginx_secrets:
```

 
 
- After the update we need to create a database in local environment. To create a database follow the next step (make sure that Docker desktop is up and running).

- Create a Database in your local with the following commands (write without $ sign).
```
$ docker-compose up --build
$ docker-compose start db 
$ docker exec -it core_db bash
$ psql -U postgres
$ CREATE DATABASE eventify;
$ \l  (to check if the database is created).
```

- After creating a database, write “docker-compose up --build” in your terminal. Check if the containers are up and running.
- Create Super User (for Admin page) with this commands
```
docker ps -a
```
fetch the container id from above command and copy it. We will use it in the command below.
```
docker exec -it <copy container id> python manage.py createsuperuser
```
and the terminal will ask the questions below, feel free to enter anything. We will present arbitrary values.
```
- Username (leave blank to use 'root'): manager
- Email address: manager@mail.com
- Password: Qrp123!
```
- Go to your local host port 80 in the browser, 127.0.0.1:80
