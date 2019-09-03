[![Build Status](https://travis-ci.com/uw-it-aca/admissions-cohort-manager.svg?branch=master)](https://travis-ci.com/uw-it-aca/admissions-cohort-manager)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/admissions-cohort-manager/badge.svg?branch=master)](https://coveralls.io/github/uw-it-aca/admissions-cohort-manager?branch=master)

# admissions-cohort-manager

Admissions Cohort Manager

System Requirements
-------------------
* Python (3+)
* Django (2+)
* Docker
* Node

Docker
------

1. Clone the repository

        $ git clone https://github.com/uw-it-aca/admissions-cohort-manager.git
        $ cd admissions-cohort-manager

2. Docker/Docker Compose is used to containerize your local build environment
    and deploy it to a local container so you can view your application. Docker
    is configured to build an empty 'project' and copy the settings files located
    in the 'docker' directory.

        $ docker-compose up

3. In the case that changes are made to the Dockerfile or docker-compose.yml file,
    you will need to rebuild the image. In this case, 'app' is the name of the
    Docker image for the Django project.

        $ docker-compose up --build

4. View your application

        Demo: http://localhost:8000/
