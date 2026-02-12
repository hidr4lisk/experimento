web: gunicorn experimento.wsgi --log-file -
release: python manage.py migrate && python init_users.py
