# Shopping List Web Application 

![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue?style=plastic)


## Table of contents 
- [Introduction](#Introduction)
 - [Fatures](#Features)
 - [Technologies](#Technologies)
- [Set Up](#SetUp)
 - [Native service in Ubuntu](#NativeserviceinUbuntu)
   - [Installation and usage for developpement](#Installationandusagefordeveloppement)
   - [Installation for production](#Installationforproduction)
   - [Usage in production](#Usageinproduction)
 - [Docker containers](#Dockercontainers)
  - [Installation and usage](#Installationandusage)
- [Source](#Source)
- [Contact](#Contact)

## Introduction 
This is the server of a web application where you can create your shopping lists (SL). You can create several SLs and add items to it of different types. At the end of the SL you'll have the calculation of the final price and the total quantity of items added. I give two posibilities for the deployment set up: Docker containers and native service.

<img src="shoppinglist/static/images/ladingpage.png" width="400"> <img src="shoppinglist/static/images/listspage.png" width="400"> 
<img src="shoppinglist/static/images/listdetails.png" width="400"> <img src="shoppinglist/static/images/userdetails.png" width="400"> 

#### Features 
- Lists creation and mathematical calculation of item's price
- Easily share lists with other users
- User authentication 

#### Technologies 
- Python 3.8.2
- Django 3.1
- django-crispy-forms 1.9.2
- Bootstrap 4
- uWSGI >=2.0.18,<2.1
- Nginx
- Docker
- Docker-compose 
- PostgreSQL (psycopg2-binary 2.8.5)

## Set Up 
This project was made to be deploy on Ubuntu OS (), where Nginx is used as proxy and as a server for static files, with the Django web framework and uWSGI as the web server gateway interface. 
The server configuration can be launched in both developpement and production stage. Two ways to set up the application for deployement where developed: 

### Native service in Ubuntu 
The first set up is made by excuting an script that configures the machine with all the necessary requirements and creates a systemd service file to launch the web application as a service, starting uWSGI when the system boots.

It uses sqlite3 as database. 

##### Instalation and usage for developpement
In the command line: 
- Clone the repository
```sh
git clone https://github.com/lizzieb1416/shopping_list_django_project.git
```
- Create and activate the virtual envirorment
```
sh python3 -m venv myenv
```
```sh
./myenv/Scripts/activate
```
- Install the requirements
```sh
pip install requirements-dev.txt
```
- Make migrations to the database 
```sh 
python manage.py makemigrations
```
```sh 
python manage.py migrate
```
- Launch the server in developpement stage
```sh
python manage.py runserver
```

##### Installation for production 
In the command line:
- Update and upgrade the machine
  ```sh
  apt-get update
  ```
  ```sh
  apt-get upgrade
  ```
- Clone the repository
  ```sh
  git clone https://github.com/lizzieb1416/shopping_list_django_project.git
  ```
  ```sh
  cd shopping_list_django_project
  ```
- Set and environment variable for `ALLOWED_HOSTS`
  ```sh
  export ALLOWED_HOSTS=<ip_machine>
  ```
- Launch the script
  ```sh
  ./launch_sl_emp_mode.sh
  ```
The service is now active in the machine for production.You can now visit <ip_machine>:80 in you browser. Changes can be made directly to the app code if necessary while it in production stage and there's no need to stop the service or reload it. With 	this configuration uWSGI will start up when the system boots.

#### Usage in production 
- To see the status of the service
  ```sh
  systemctl status emperor.uwsgi.service
  ```
- To stop the service
  ```sh
  systemctl status emperor.uwsgi.service
  ```
- To start the service
  ```sh
  systemctl start emperor.uwsgi.service
  ```
- To delete the service from the machine
  ```sh
  sudo ./clean.sh 
  ```

### Docker containers
The second one uses Docker containers and Docker Compose to run the application. There is two Docker images, one with the web application and the database and the other one with Nginx.

It uses PostgreSQL as database. 

#### Instalation and usage
- update and upgrade the machine
  ```sh
  apt-get update
  ```
  ```sh
  apt-get upgrade
  ```
- Clone the repository
  ```sh
  git clone https://github.com/lizzieb1416/shopping_list_django_project.git
  ```
  ```sh
  cd shopping_list_django_project
  ```
- Install Docker and Docker Compose
  ```sh
  sudo apt install docker.io
  ```
  ```sh
  sudo apt install docker-compose
  ```
- Launch for development
  ```sh
  docker-compose up
  ```
  Connect to it in the browser tapping `<localhost_ip>:8000`
- Launch for production 
  ```sh 
  docker-compose -f docker-compose-deploy.yml up
  ```
  Connect to it in the browser tapping `<localhost_ip>:8000`
 
## Source 
 
- [Django tutorial - Tech with Tim](https://www.techwithtim.net/tutorials/django/setup/)
- [How to set up Django on Nginx with uWSGI - Tony Teaches Tech](https://tonyteaches.tech/django-nginx-uwsgi-tutorial/)
- [Prepare a Django app for Deployment using Docker - London App Developer](https://www.youtube.com/watch?v=nh1ynJGJuT8&list=PLIWLW8_gNNc1dLUGuSAzpsf3zRDrR-yKy&index=45&t=1893s)


## Contact 
Liset Bastidas - lisetbastidasg@gmail.com
