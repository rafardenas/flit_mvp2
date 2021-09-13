python manage.py collectstatic --no-input

python manage.py runserver 

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

gunicorn --worker-tmp-dir /dev/shm djcrm.wsgi
