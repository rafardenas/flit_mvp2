python3 manage.py collectstatic --no-input

DJANGO_SETTINGS_MODULE=djcrm.settings 
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=:"${PYTHONPATH}:/Users/Rafa/opt/anaconda3/envs/django/bin"

python3 manage.py migrate 

gunicorn --worker-tmp-dir /dev/shm djcrm.wsgi:application
