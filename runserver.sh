python manage.py collectstatic --no-input

python manage.py migrate

gunicorn --env DJANGO_SETTINGS_MODULE=djcrm.settings --worker-tmp-dir /dev/shm djcrm.wsgi:application
