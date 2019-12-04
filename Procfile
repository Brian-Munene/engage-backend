web:  gunicorn venv.app.routes:app
release: python manage.py db init; db migrate; db upgrade