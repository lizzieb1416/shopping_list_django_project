#!/usr/bin/env bash

set -e

FILE=/etc/systemd/system/emperor.uwsgi.service
if [ -f "$FILE"]; then
	echo "$FILE exists, reconfiguring the service..."
	sudo rm -f /etc/nginx/sites-available/sl.conf
	sudo rm -f /etc/nginx/sites-enabled/sl.conf
	sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
	
	sudo rm -rf sl-env
	
	sudo systemctl stop emperor.uwsgi.service
	sudo systemctl disable emperor.uwsgi.service
	sudo rm -f /etc/systemctl/system/emperor.uwsgi.service
	sudo pkill -f uwsgi -9
else 
	echo "Starting service configuration"
fi

export SHOPPINGLIST_DIR=$PWD

if [[ -z "${ALLOWED_HOSTS}" ]]; then
  echo "Please set ALLOWED_HOSTS environment var with the IP of this machine"
  exit 1
fi

# Installation of packages
echo "STEP 1/9: installing pre-requisites..."
sudo apt-get install -y python3.8 python3-venv python3.8-dev gcc nginx git

# Envirorment creation and installation of python packages
echo "STEP 2/9: creating environment"
python3 -m venv sl-env
. ./sl-env/bin/activate
python3 -m pip install -r ./requirements.txt 

# set env variables for settings.py 
echo "STEP 3/9: exporting environment variables for settings.py"
sed -i "s/ALLOWED_HOSTS\ =\ \[\]/ALLOWED_HOSTS\ =\ [\'$(echo $ALLOWED_HOSTS)\']/g" $SHOPPINGLIST_DIR/shoppinglist/shoppinglist/settings.py
export DEBUG=0 

# Nginx configuration 
echo "STEP 4/9: setting up Nginx"
sed -i "s/DIRECTORY/$(echo $SHOPPINGLIST_DIR | sed "s/\//\\\\\//g")/g" $SHOPPINGLIST_DIR/deploy_emperor_mode/nginx/sl.conf   ####!!!
sudo ln -s $SHOPPINGLIST_DIR/deploy_emperor_mode/nginx/sl.conf /etc/nginx/sites-available  ######!!
sudo ln -s /etc/nginx/sites-available/sl.conf /etc/nginx/sites-enabled/sl.conf
sudo rm -f /etc/nginx/sites-enabled/default

# Put static files in its place and restart the server
echo "STEP 5/9: collecting static files for Shopping List"
#python3 $SHOPPINGLIST_DIR/shoppinglist/manage.py makemigrations
#python3 $SHOPPINGLIST_DIR/shoppinglist/manage.py migrate
python3 $SHOPPINGLIST_DIR/shoppinglist/manage.py collectstatic --noinput

echo "STEP 4.1/10: Installing postgreSQL "
sudo apt-get install libpq-dev
sudo apt install postgresql postgresql-contrib
echo "STEP 4.2/10: Creating user for the database"
sudo -u postgres createuser $USER -s
echo "STEP 4.3/10: Creating database: sl_db"
sudo -u postgres createdb sl_db
#echo "STEP 4.4/10: Linking database to user"
#psql -d sl_db
echo "STEP 4.4/10: Migrating to database"
python3 $SHOPPINGLIST_DIR/shoppinglist/manage.py makemigrations
python3 $SHOPPINGLIST_DIR/shoppinglist/manage.py migrate

echo "STEP 6/9: restarting Nginx server"
sudo /etc/init.d/nginx restart

# Conf for emperor mode
echo "STEP 7/9: setting up emperor mode"
sed -i "s/DIRECTORY/$(echo $SHOPPINGLIST_DIR | sed "s/\//\\\\\//g")/g" $SHOPPINGLIST_DIR/deploy_emperor_mode/sl_uwsgi.ini  #####!!!
mkdir $SHOPPINGLIST_DIR/sl-env/vassals 
sudo ln -s $SHOPPINGLIST_DIR/deploy_emperor_mode/sl_uwsgi.ini $SHOPPINGLIST_DIR/sl-env/vassals

# symbolic link to create service to launch the sl when the system boots
echo "STEP 8/9: creating Shopping List service"
sed -i "s/DIRECTORY/$(echo $SHOPPINGLIST_DIR | sed "s/\//\\\\\//g")/g" $SHOPPINGLIST_DIR/deploy_emperor_mode/emperor.uwsgi.service #####!!!
sed -i "s/temporarystuff/$(echo $USER)/g" $SHOPPINGLIST_DIR/deploy_emperor_mode/emperor.uwsgi.service  ###!!!!
#sudo ln -s $SHOPPINGLIST_DIR/emperor.uwsgi.service /etc/systemd/system
sudo cp $SHOPPINGLIST_DIR/deploy_emperor_mode/emperor.uwsgi.service /etc/systemd/system

# Enable service
echo "STEP 9/9: enable service"
sudo systemctl enable emperor.uwsgi.service
sudo systemctl start emperor.uwsgi.service


echo "Shopping List installed and available at http://$ALLOWED_HOSTS with your browser"
