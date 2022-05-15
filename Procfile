release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn core.wsgi
worker: python worker.py
worker: celery -A core worker -B --loglevel=info