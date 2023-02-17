# Work Balancer API

* Coverage threshold in CI > 90%
## About
The WorkBalancerApi is a backend service of the [WorkBalancer](https://github.com/nikitazigman/WorkBalancer) project. 

The API has 2nd maturity level of [the Richardson REST Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html). The backend provides endpoints for [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) tasks and days as well as endpoints for Authorization and Authentication. 

The API utilizes [PostgreSQL DBMS](https://www.postgresql.org/). 

The service is written as a monolith due to the fact there are no demands to handle the huge load and currently, I am a single person which maintains the App. Nevertheless, the project was structured in a way to easily break down into a set of WEB services. Hopefully, one day it would make sense :). 

The service uses [JWT](https://jwt.io/introduction) authentication method. Both tokens are stored in the cookies.  

## Structure of the repository: 
``` bash
WorkBalancerAPI/ # Root directory of the repository
    .github/ # CI yaml config for the github
    .vscode/ # VS code editor configs 
    config/ # contains all configurational files for production deployment
        gunicorn/ # contains gunicorn config python script 
        nginx/ # nginx config 
        prod_env/ # here you should be placed .env file for production deployment
    doc/ # materials for the readme.md file
    service/ # root of the Django project 
        day/ # django application contains all logic related to the days
        task/ # django application contains all logic related to the tasks
        user/ # django application contains all logic related to the users
        service/ # django core folder 
        django_config/ # here should be stored all django related configs (.env)
    # docker compose, docker, pre-commit conf license and other support files for linter and fixers.
```

## Utilized technologies: 
The service is written on the [Django WEB framework](https://www.djangoproject.com/#:~:text=Django%20is%20a%20high%2Dlevel,It's%20free%20and%20open%20source.). Below you can find the list of the main technologies which extend the functionality of the framework and the purpose of using them in the project. For the full list of dependencies, you can check the [requirements.txt](requirements.txt)

* [Django REST framework](https://www.django-rest-framework.org/) was used to implement the REST API. 
* [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/) and [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) extend the rest framework to provide REST API registration and authorization endpoints. The lib is configured to use [JWT](https://jwt.io/introduction) authorization, where the access and refresh tokens are stored in the cookies. Check [settings](service/service/settings.py) to see the configuration. 
* [django-filter](https://django-filter.readthedocs.io/en/stable/) extends the rest framework. It is used to let a client to filter tasks and days.
* [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) is used to dynamically generate openapi human-readable schema. 
* [pytest-django](https://pytest-django.readthedocs.io/en/latest/) allows using the pytest lib instead of Django "manage.py test". It is more convenient especially if you are working in vs code editor. 
* [gunicorn](https://gunicorn.org/) is python [WSGI]() server. The Django app is called by the gunicorn in the production setup.  
* [django-cors-headers](https://pypi.org/project/django-cors-headers/) is used for test purposes only. It allows resources to be accessed from a different domain. It is quite convenient when one develops the front-end part.

## API schemas:
Depending on your preferences, you can use auto-generated static yaml openapi-schema or a dynamically generated redoc page. Both ways are equivalent the only difference is the representation. 

The yaml schema is located in [doc/openapi-schema.yml](doc/openapi-schema.yml). 

To get access to the /redoc page complete the following steps:
1. Install docker and docker-compose on your machine. The easiest way to do so is to follow the [instruction](https://docs.docker.com/get-docker/).
2. Run docker engine or docker desktop on your machine
3. Go to the root directory of the repository 
4. Run a test docker compose file to launch a test environment.  
``` bash
# -d runs it as a daemon 
docker-compose -f docker-compose-test.yaml up -d 
```
or if you installed docker compose as an extension 
``` bash
# -d runs it as a daemon 
docker compose -f docker-compose-test.yaml up -d 
```
5. Open your favorite WEB browser and go to the "http://localhost/redoc/". You should see something like this ![screenshot of the redoc page](/doc/redoc-screenshot.png)
6. To stop the environment simply run the following command.
``` bash
# -d runs it as a daemon 
docker-compose -f docker-compose-test.yaml down
```
or if you installed docker compose as an extension 
``` bash
# -d runs it as a daemon 
docker compose -f docker-compose-test.yaml down 
```

## Custom commands

``` bash
# generates dummy data in the db for test purpose only
python manage.py generate_test_data

    --users_quantity int
    --days_per_user int
    --max_tasks_per_day int
```

## ToDo:
* A user can get information about their working capacity based on completed and assigned tasks per day. 
* A user can integrate their tasks from a calendar, and Git platforms into the app. (The Kanban apps is questionable)
* A user can register on the service with their google account


## Technical debts:
* Cache. The load on the service is super low. Currently, I am a single user :D, but it is not cool to have a backend without cache)
* Email verification (It is necessary to get more familiar with the law before storing and sending emails)