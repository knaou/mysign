#!/bin/sh

cp -rf /app/public-src/* /app/public/

cd /app/server
python3 manage.py migrate admin
python3 manage.py migrate ca
/usr/local/bin/uwsgi --ini uwsgi.ini

