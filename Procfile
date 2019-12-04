web:  gunicorn venv.app.routes:app
release: python venv/app/manage.py db init; db migrate; db upgrade