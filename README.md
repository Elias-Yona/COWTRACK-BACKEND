# QUICKSTART

1. Make sure you have installed MySQL. Follow this URL for a detailed guide [mysql](https://dev.mysql.com/downloads/)

2. On your MySQL server create a database called `cowtrack`. You can run the following commands

```bash
mysql -u [username] -p [password]

CREATE DATABASE cowtrack
```

3. Install poetry. Follow this URL for a detailed guide [poetry](https://python-poetry.org/docs/#installation)

4. Clone the repository

```bash
git clone https://github.com/Elias-Yona/COWTRACK/ && cd COWTRACK
```

5. Run the following command to install project dependencies

```bash
poetry install
```

6. Apply the migration files to your database

```bash
poetry run python manage.py migrate
```

7. Run the following command to start the development server

```bash
poetry run python manage.py runserver
```

8. Open the following URL [localhost:8000](http://127.0.0.1:8000/)
