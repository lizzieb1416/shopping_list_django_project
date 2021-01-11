#!/bin/sh

rm -rf /etc/nginx/sites-available/sl.conf
rm -rf /etc/nginx/sites-enable/sl.conf
ln -s /etc/nginx/sites-enable/default /etc/nginx/sites-available/default

rm -rf sl-env

systemctl diable emperor.uwsgi.service
