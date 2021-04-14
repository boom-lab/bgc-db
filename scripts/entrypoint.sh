#!/bin/sh

#stops and exits if error, does not run remainder of commands
set -e

#moves all static files to one location
python manage.py collectstatic --noinput

#starts django app in uwsgi service
uwsgi --socket :8000 --master --enable-threads --module bgc-db.wsgi