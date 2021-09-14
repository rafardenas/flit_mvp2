python3 manage.py collectstatic --no-input

python3 manage.py migrate

gunicorn --env DJANGO_SETTINGS_MODULE=djcrm.settings djcrm.wsgi
