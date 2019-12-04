web:  gunicorn venv.app.routes:app
release: python venv/app/manage.py db init; python venv/app/manage.py db migrate; python venv/app/manage.py db upgrade