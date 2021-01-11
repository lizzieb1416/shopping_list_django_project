#!/bin/sh

rm -f /etc/nginx/sites-available/sl.conf
rm -f /etc/nginx/sites-enabled/sl.conf
rm -f /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

rm -rf sl-env

systemctl disable emperor.uwsgi.service
