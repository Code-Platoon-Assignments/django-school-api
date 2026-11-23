
# School API

By the end of this assignment you will have a fully serviceable CRUD API with user authentication capabilities that will allow School staff to easily manage students and schollastic equipment.

## Student Model

In this assignment we will create a Student Django Model with the following fields

| field            | required |type |example data                    |
| ----------------- | -----|-------|------------- |
| name | True |string | John W. Watson |
| student_email | True | string(email) | johnnyBoy@school.com |
| personal_email | False | string(email) | johnnyBoy@gmail.com |
| locker_number | True |int |137 |
| locker_combination | True |string |37-68-98 |
| good_student | True |boolean | True |

## Django Set Up

This project runs as **two containers** (Django and PostgreSQL) managed by Docker Compose, following the setup from the *Intro to Django* lesson.

### 1. Project structure

Create the following structure at the root of this repository:

```bash
django-school-api/
├── db/
│   └── Dockerfile
├── server/
│   ├── Dockerfile
│   └── .dockerignore
└── docker-compose.yml
```

```bash
mkdir -p db server
touch db/Dockerfile server/Dockerfile server/.dockerignore docker-compose.yml
```

`db/Dockerfile`

```Dockerfile
FROM postgres:15

ENV POSTGRES_USER=cp_user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=school_db

EXPOSE 5432

CMD ["postgres"]
```

`server/Dockerfile`

```Dockerfile
FROM python:3.15.2-slim-trixie

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

`server/.dockerignore`

```
.venv/
__pycache__/
db.sqlite3
```

`docker-compose.yml`

```yml
services:
  db:
    build: ./db
    ports:
      - "5433:5432"
    volumes:
      - school_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cp_user -d school_db"]
      interval: 5s
      timeout: 5s
      retries: 10

  backend:
    build: ./server
    ports:
      - "8000:8000"
    volumes:
      - ./server:/app
    depends_on:
      db:
        condition: service_healthy

volumes:
  school_data:
```

### 2. Virtual environment and Django project

Everything Python related lives inside `server`. Create and activate a virtual environment there:

```bash
cd server

#creating and activating venv
python3 -m venv .venv && source .venv/bin/activate
```

Install Django and psycopg (the driver Django uses to speak with PostgreSQL), then record your dependencies:

```bash
pip install django "psycopg[binary]"
pip freeze > requirements.txt
```

Create the project and the student app. **Don't forget the period!**

```bash
django-admin startproject school_proj .
python manage.py startapp student_app
```

### 3. Configure `settings.py`

- Add `student_app` under `INSTALLED_APPS`.
- Set `ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']`
- Replace SQLite with the PostgreSQL service:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'school_db',
        'USER': 'cp_user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

`HOST` is `db` because that is the **service name** in `docker-compose.yml`, and `PORT` is `5432` because Django talks to PostgreSQL container-to-container.

### 4. Start the containers

From the root of the repository (where `docker-compose.yml` lives):

```bash
docker compose up -d --build
```

Django commands must run **inside** the `backend` container:

```bash
docker compose exec backend bash
```

Once the Student Model is completed, makemigrations and migrate to the school_db (inside the container)

```bash
python manage.py makemigrations
python manage.py migrate
```

When you are done for the day, run `docker compose down` (add `-v` only if you want to delete the database).

> Whenever you `pip install` a new package, run `pip freeze > requirements.txt` in `server/` and then `docker compose up -d --build`.

## Running Tests

Replace the `test.py` file inside your app with the `test.py` file already attached to this repository.

Now you can run the test suite by typing the following **inside the `backend` container**

```bash
  python manage.py test
```

- `.` means a test passed
- `E` means an unhandled error populated on a test
- `F` means a test completely failed to run
