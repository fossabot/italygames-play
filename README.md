# ItalyGames Play
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Facifani%2Fitalygames-play.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Facifani%2Fitalygames-play?ref=badge_shield)


A bunch of us over at italygames felt the necessity to create a tool that would 
let us find other gamers to play with. [Play](https://play.italyga.me) is born 
from this idea and we hope it will help bring gamers from reddit closer together.

[Come join us](https://play.italyga.me).

## Development
Play is completely open source and on its early stages of development so we 
would love if you could help it grow by contributing.
Play is being developed using [Flask](http://flask.pocoo.org/) 
and [Bootstrap](https://getbootstrap.com/). 
We also would like to thank all the awesome people that developed the open source 
libraries we are currently using:
[Flask-Login](https://flask-login.readthedocs.io/en/latest/),
[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/),
[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/),
[Flask-Script](https://flask-script.readthedocs.io/en/latest/),
[Flask-Testing](https://pythonhosted.org/Flask-Testing/),
[Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/),
[coverage](https://coverage.readthedocs.io/en/coverage-4.4.1/),
[gunicorn](http://gunicorn.org/),
[rauth](https://rauth.readthedocs.io/en/latest/).


### Prerequisites

* Python, virtualenv is recommended
* MySQL and/or SQLite
* Register a Reddit web app [here](https://www.reddit.com/prefs/apps)

Please note that in order to use another DB you would need to check for SQLAlchemy 
support and install dependencies accordingly.

### Setup

#### Virtualenv
Get a copy of the source code

```
$ git clone https://github.com/acifani/italygames-play.git
```

Setup virtualenv
```
$ cd italygames-play
$ virtualenv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

#### Environment variables
You need to setup the following environment variables (`export VARIABLE=VALUE` if on Linux)

`FLASK_CONFIG`: Set to either `development`, `testing` or `production` based on your environment. You can add more config sets in `config.py`.

`FLASK_APP`: File that contains the app (not the app factory), in our case `manage.py`.

`SECRET_KEY`:  Secret key needed by Flask to handle Sessions encryption. [Check Flask Sessions docs](http://flask.pocoo.org/docs/0.12/quickstart/#sessions).

`DEV_DB_URI` `TEST_DB_URI` `DB_URI`: Database URLs, if not set defaults to SQLite. You can modify defaults in `config.py`.

`OAUTH_REDDIT_ID` `OAUTH_REDDIT_SECRET`: The reddit app ID and Secret key, you can get those [here](https://www.reddit.com/prefs/apps) after you register your app.

#### Database first time setup
```
(venv)$ python manage.py create_db
(venv)$ python manage.py db stamp head
```

### Run

#### Development server
```
(venv)$ python manage.py runserver
```

[Flask built-in development server](http://flask.pocoo.org/docs/0.12/server/): 
do NOT use for production as it is not build to manage more than one request at the time.

#### Production server
```
(venv)$ python manage.py gunicorn
```
[Gunicorn](http://gunicorn.org/) WSGI HTTP server.

Optional parameters:

* `-w`  `--workers` Number of worker threads to use. Gunicorn [recommends](http://docs.gunicorn.org/en/stable/design.html#how-many-workers) to set this to `(2 x $num_cores) + 1`.

* `-p`  `--port` Port number. Also supports Unix sockets.

* `-h`  `--host` Host address.

### Test
```
(venv)$ python manage.py test
```
Run the test with `unittest`.

Optional parameters:
* `-c` `--coverage`: Shows `coverage` report and generates HTML version inside `tmp` folder.

### Database migrations
Database migrations and updates are managed with [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) 
that works on top of [Alembic](http://alembic.zzzcomputing.com/en/latest/). Please read the docs carefully.

You can use `python manage.py db` to access all the Flask-Migrate CLI commands.

Usually when you make a Model change you want to run `python manage.py db migrate` 
to generate migration scripts inside `migrations/versions`. Check those and if OK
run `python manage.py db upgrade` to execute the changes on the database.

### Docker
More info on how to build and deploy with Docker and docker-compose will be added Soon™.

## Contacts
If you have any question or feedback please do get in touch with us on:
* [Subreddit](https://www.reddit.com/r/italygames/) /r/italygames
* [Telegram](https://t.me/joinchat/AAAAAEHF2KTVrbvj899Vsw) group
* [Discord](https://discord.gg/4SYwXK8) room

## License
The content of this project itself is licensed under the 
[Creative Commons Attribution 3.0 license](https://creativecommons.org/licenses/by/3.0/), 
and the underlying source code used to format and display that content is licensed 
under the [MIT License](https://opensource.org/licenses/MIT).


[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Facifani%2Fitalygames-play.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Facifani%2Fitalygames-play?ref=badge_large)