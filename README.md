codeflix
========
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.txt)
[![pipeline status](https://gitlab.crans.org/bombar/codeflix/badges/master/pipeline.svg)](https://gitlab.crans.org/bombar/codeflix/commits/master)
[![coverage report](https://gitlab.crans.org/bombar/codeflix/badges/master/coverage.svg)](https://gitlab.crans.org/bombar/codeflix/commits/maste)

Required packages
-----------------

 * python3
 * python3-django
 * python3-dev
 * python3-psycopg2
 * postgresql
 * nginx
 * uwsgi
 * uwsgi-plugin-python3
 * python3-venv
 * memcached
 * gettext

## Install

First, clone the project (For instance in `/var/www/codeflix/`)

	$ git clone https://gitlab.crans.org/bombar/codeflix.git

### Install dependencies

	$ sudo apt install python3
    $ sudo apt install python3-venv
	$ sudo apt install python3-dev
    $ sudo apt install postgresql
	$ sudo apt install postgresql-server-dev-NN # Where NN is the postgresql version.
	$ sudo apt install gcc # Needed to compile python packages
	$ sudo apt install memcached # Needed for caching (autocompletion)
	$ sudo apt install gettext # Needed for translation

	$ python3 -m venv venv
	$ source venv/bin/activate
    $ pip3 install -r requirements.txt


### Setup the backend

We use a Postgresql Database Engine. By default the database name is `codeflix` and so is the database user, and is accessed locally. But this can be changed in `codeflix/codeflix/settings_local.py`. In this very same file, setup

	$ mpasswd # Create a password for the database user and put it in settings_local.py
	$ sudo -u postgres psql
	postgres=# CREATE ROLE codeflix LOGIN PASSWORD 'VerySecretPassword';
	postgres=# CREATE DATABASE codeflix OWNER codeflix;

You may need to allow the user <codeflix> to connect to the database <codeflix>, according to your infrastructure. Please refer to the [PostgreSQL documentation](https://www.postgresql.org/docs/) for more information.

For instance, on a fresh install on a Debian Buster-Like server, you may edit the file `/etc/postgresql/11/main/pg_hba.conf` and add the line

	local codeflix codeflix        md5


Generate a new `secret_key` for the project, and put it in `codeflix/codeflix/settings_local.py` :

	$ python3 -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%&*(-_=+)") for i in range(50)]))'

Finally, apply the migrations

	$ cd codeflix
	$ ./manage.py makemigrations
	$ ./manage.py migrate


### Run a demo server

	$ ./manage.py runserver


### Create a superuser

	$ ./manage.py createsuperuser


### Setup the website on a real server

We provide an example configuration to use with `Nginx` webserver and `uWSGI`.

#### Configuration for uWSGI and Nginx

First, install the necessary packages. For instance, on a Debian-like server

    $ sudo apt install nginx uwsgi uwsgi-plugin-python3

Then, edit the example configuration located in `codeflix/utils/` with your parameters.

Finally, link the files to `Nginx` and `uWSGI` configuration

For example :

    $ sudo ln -s /var/www/codeflix/utils/codeflix_nginx.conf /etc/nginx/sites-enabled/
    $ sudo ln -s /var/www/codeflix/utils/codeflix_uwsgi.ini /etc/uwsgi/apps-enabled/
    $ sudo systemctl restart nginx uwsgi

#### HTTPS

If you want to use HTTPS (and you should !), you need to create certificates. We advise you to use Let's Encrypt certificates. Please, refer to the corresponding documentation for more information.

#### Local Settings

You will also need to edit your `settings_local.py` to provide a list of `ALLOWED_HOSTS` and a path for the static files.

Finally, collect the static files and make the translations.

    $ ./manage.py collectstatic
    $ ./manage.py compilemessages
