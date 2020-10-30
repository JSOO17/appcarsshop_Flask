# Shoping Cart Base
This is the root app to start the project, is mounted on Python 3.7 with
cutting edge Flask, Flask-alchemy and Flasks Migrations.
This App is mounted on Docker and Docker Compose, to run it please run:

```
docker-compose up
```

It will take the changes on the code and reload the container with the new ones

To install the packages locally first install pipenv
```
pip install pipenv
```
And then run 
```
pipenv install
```

## TO Create Tables on DB
Right now this projects has a SQLLite DB, pointing to **/api/data/app.db** 
To change the file or perform an init of the migrations use
```
flask db init
```
To perform a migration
of new tables please use
```
flask db migrate -m "model table"
```
Then:
```
flask db upgrade
```
