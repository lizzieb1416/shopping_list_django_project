#!/bin/sh

set -e

echo "Waiting for postgres .."
while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"


python manage.py makemigrations 
python manage.py migrate
python manage.py collectstatic --noinput

uwsgi --socket :8000 --master --enable-threads --module shoppinglist.wsgi
