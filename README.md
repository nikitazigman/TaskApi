[![Django CI](https://github.com/nikitazigman/work_balancer/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/nikitazigman/work_balancer/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/nikitazigman/work_balancer/branch/master/graph/badge.svg?token=I5U9GK3W1O)](https://codecov.io/gh/nikitazigman/work_balancer)
# Work Balancer Back-end

## About

Work balancer is a web application that will help you to understand how many task you can do per a day.
Why is it necessary?\

* It allows you to increase your work planning accuracy. The more linear your working activity the easier define deadlines.
* It reduces your working stress, over work and in the end burnout.
* It has positive effect on your personal brand. Your clients will be more confident in work with you if they would see you as well-organised employee.

Therefore, you can consider the application as a way to understand yourself and tune your working activity, to make yourself more efficient.

## Documentation

### The list of API endpoints:

| Endpoint                                   | HTTP Verb                    |
|--------------------------------------------|------------------------------|
| api/v1/task/<int:pk>                       | GET, POST, PUT, PATCH, DEL   |
| api/v1/task/create                         | POST                         |
| api/v1/tasks                               | GET                          |
| api/v1/lists                               | GET, POST                    |
| api/v1/list/create                         | POST                         |
| api/v1/dj-rest-auth/registration           | POST                         |
| api/v1/dj-rest-auth/login                  | POST                         |
| api/v1/dj-rest-auth/logout                 | GET                          |
| api/v1/dj-rest-auth/password/reset         | POST                         |
| api/v1/dj-rest-auth/password/reset/confirm | POST                         |

The full documentation you can find [here](doc/openapi-schema.yml)

**You can run the service and open /redoc endpoint**

#### GET api/v1/tasks

You can add following filters to the request:

| Arg's name        | data format       | Description                                   |
|-------------------|-------------------|-----------------------------------------------|
| is_active         | bool              | return tasks with given is_active value       |
| list_id           | int               | return tasks with given list_id               |
| deadline_after    | Date 'yyyy-mm-dd' | return tasks with deadline after given date   |
| deadline_before   | Date 'yyyy-mm-dd' | return tasks with deadline after given date   |
| excluded_list_id  | int               | return tasks with list_id != excluded_list_id |

example:

    GET /api/v1/tasks/?is_active=true&deadline_after=2021-06-25&excluded_list_id=1

#### CRUD api/v1/task/<int:pk>

JSON Properties:

| property name     | data format       | Description                                   |
|-------------------|-------------------|-----------------------------------------------|
| title         | str               | title of the task < 50    |
| description   | str               | description of the task   |
| comments      | str               | comments of the task      |
| is_active     | bool              | task's status             |
| difficulty    | int               | task's difficulty         |
| deadline      | Date 'yyyy-mm-dd' | task's deadline           |
| list_id       | int               | task's list, can be Null  |

example:

    POST /api/v1/task/1/
    content_type = application/json

    {
        "id": 1,
        "title": "1",
        "description": "1",
        "comments": "1",
        "is_active": true,
        "difficulty": 1,
        "number_of_movements": 0,
        "deadline": "2021-09-24",
        "list_id": 1
    }

### The database schema:

![db structure](doc/my_project_visualized.png)

## How to launch
Start:
```commandline
    docker-compose up -d --build
```
Migrations:
```commandline
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
```
Create superuser
```commandline
    docker-compose exec web python manage.py createsuperuser
```
Then go to the\
[localhost:8000](localhost:8000)

Stop
```commandline
    docker-compose down
```
