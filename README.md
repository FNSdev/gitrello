# GITrello

[![Build Status](https://gitrello.me/jenkins/buildStatus/icon?job=gitrello)](https://gitrello.me/jenkins/job/gitrello/)

## How to run locally

### Tested on

* Linux Mint 19.3
* Python 3.8.5
* Poetry 1.1.4
* Docker 19.03.14
* Docker-Compose 1.26.0

### 1. Install required libraries

```
$ sudo apt install libpq-dev git gcc libc6-dev
```

### 2. Clone repository

```
$ git clone https://github.com/FNSdev/gitrello.git
$ cd gitrello
```

### 3. Create virtual environment

Consider using `pyenv` and `pyenv-virtualenv`

```
$ pyenv virtualenv 3.8.5 gitrello
$ pyenv local gitrello
```

### 4. Install dependencies

```
$ poetry install
```

### 5. Run database using Docker-Compose

#### 5.1. Launch containers

```
$ docker-compose up
```

#### 5.2. Initialize cluster

```
$ docker exec -it roach_1 ./cockroach init --insecure
```

#### 5.3. Create database & user

```
$ docker exec -it roach_1 ./cockroach sql --insecure
```

```sql
create database gitrello;
create user gitrello;
grant all on database gitrello to gitrello;
grant admin to gitrello;
```

### 6. Create .env file

It should be OK to use default values for now.

```
$ cp .env.local .env
```

### 7. Apply migrations

```
$ cd gitrello
$ python manage.py migrate
```

### 8. [OPTIONAL] Run test

```
$ python manage.py test
```

### 9. Run server

```
$ python manage.py runserver
```

### 10. [OPTIONAL] Configure integration with GitHub

#### 10.1. Set-up and run Gitrello-GitHub-Integration-Service

Follow instructions in https://github.com/FNSdev/gitrello-github-integration-service

#### 10.3. Create GitHub Oauth application

Visit https://github.com/settings/developers to create a new Oauth application. 
Remember it's `client_id` and `client_secret`.

#### 10.2 Configure ENV variables

* GITHUB_INTEGRATION_SERVICE_URL - http://0.0.0.0:8001 by default
* GITHUB_INTEGRATION_SERVICE_TOKEN - Should be the same as GITRELLO_ACCESS_TOKEN in gitrello-github-integration-service
* GITHUB_CLIENT_ID - use value from the previous step
* GITHUB_CLIENT_SECRET - use value from the previous step
