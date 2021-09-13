python manage.py collectstatic --no-input

DJANGO_SETTINGS_MODULE=djcrm.settings 
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

python3 manage.py migrate 

gunicorn --worker-tmp-dir /dev/shm djcrm.wsgi
