codeflix
========

Required packages
-----------------

 * python3
 * python3-django
 * python3-psycopg2
 * postgresql
 * nginx
 * uwsgi
 * uwsgi-plugin-python3
 * python3-venv

## Install

First, clone the project (For instance in `/var/www/codeflix/`)

	$ git clone https://gitlab.crans.org/bombar/codeflix.git

### Setup virtualenv

	$ python3 -m venv venv
	$ source venv/bin/activate


### Setup the backend

We use a Postgresql Database Engine. By default the database name is `codeflix` and so is the database user, and is accessed locally. But this can be changed in `codeflix/codeflix/settings_local.py`. In this very same file, setup

	$ mpasswd # Create a password for the database user and put it in settings_local.py
	$ sudo -u postgres psql
	postgres=# CREATE ROLE codeflix LOGIN PASSWORD <password>;
	postgres=# CREATE DATABASE codeflix OWNER codeflix;

Then, you need to allow the user <codeflix> to connect to the database <codeflix>, according to your infrastructure. Please refer to the [PostgreSQL documentation](https://www.postgresql.org/docs/) for more information.

For instance, on a fresh install on a Debian Buster-Like server, you can edit the file `/etc/postgresql/11/main/pg_hba.conf` and add the line

	local codeflix codeflix        md5


Generate a new `secret_key` for the project, and put it in `codeflix/codeflix/settings_local.py` :

	$ python3 -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%&*(-_=+)") for i in range(50)]))'

Finally, apply the migrations

	$ ./manage.py makemigrations
	$ ./manage.py migrate


### Run a demo server

	$ ./manage.pu runserver
