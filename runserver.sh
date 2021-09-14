python3 manage.py collectstatic --no-input

python3 manage.py migrate

gunicorn --env DJANGO_SETTINGS_MODULE=djcrm.settings --worker-tmp-dir /dev/shm djcrm.wsgi
