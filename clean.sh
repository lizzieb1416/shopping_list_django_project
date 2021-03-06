es#!/bin/sh

rm -f /etc/nginx/sites-available/sl.conf
rm -f /etc/nginx/sites-enabled/sl.conf
rm -f /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

rm -rf sl-env

systemctl stop emperor.uwsgi.service
systemctl disable emperor.uwsgi.service
rm -f /etc/systemd/system/emperor.uwsgi.service
sudo pkill -f uwsgi -9

sudo apt-get purge postgresql*
sudo deluser postgres
sudo apt-get purge pgadmin4
