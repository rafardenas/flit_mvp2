# Flit MVP 2

First version of Flit that actually solves the trust problem 

We can use the admin page of the site to update Flit "in the back". 

### Backlog

1. Google Maps route [Link](https://www.youtube.com/watch?v=BkGtNBrOhKU)
- set lat and longitud for each trip (create fields in the db)


### Resources, problems, solutions

#### Styles

- Progress bar: https://www.creative-tim.com/learning-lab/tailwind-starter-kit/documentation/css/progressbars

#### Resources

[Dynamic Filters](https://teamtreehouse.com/community/how-to-filter-modelchoicefield-by-fields):
- Chance the options of the filters based on previous filter selections

[Make Queries](https://docs.djangoproject.com/en/3.2/topics/db/queries/)

- Query for all recors in database *"Car"*
    - Car.objects.all()
- Filters (*make is a field in the table*)
    - Car.objects.filter(make=Audi)

[Run queries with psql shell](https://courses.cs.washington.edu/courses/csep544/11au/resources/postgresql-instructions.html#psql)
    1. Open terminal and run 
    2. psql -U postgres my_database
    where my_database is the name of the database

[Basic Queries](https://www.postgresqltutorial.com/postgresql-update/)

**Set date input format in django.forms**
    add this attribute to the field:
    `input_formats=['%d/%m/%y']`


[When override the save method in django models?](https://www.sankalpjonna.com/learn-django/how-to-override-the-save-method-in-your-django-models)



**django shell**
$ python3 manage.py shell

**create superuser**
$ python3 manage.py createsuperuser

**query all (returns a QuerySet object)**
{table-name}.objects.all()

**Restrict access to a view for no-logged in users**
add the parent-class `LoginRequiredMixin` to the view classes.

**Use signals to trigger routines when a specific event takes place**

**Foreign key to non-primary key**
Can I set a column as Foreign Key even though it is not a PK of the parent table?
*short answer: Yes*
*long answer:*
https://stackoverflow.com/questions/18435065/foreign-key-to-non-primary-key

**Reverse lookup using a Foreign key**

Use case: Having 2 tables A and B, A has a Foreign Key that references to a column in B. We want to fetch all the records in table A that have a specific foreign key in table B.

1. In table a, set the attribute `related_name` in the Foreign Key (Fk) column of table A
2. Inside a `get_context` method, write:
    - `qs = self.get_object().leads.all()`
    - 'leads' being the `related_name` in the Fk column of table A
    
**Requirements file in the correct format (w/out path)**
$ `pip list --format=freeze > requirements.txt`

See more [here](https://stackoverflow.com/questions/62885911/pip-freeze-creates-some-weird-path-instead-of-the-package-version)

**Not found external django app**

Make sure the PYTHONPATH contains the directory where this external app is installed
e.g. `'crispy_forms' not found`
1. run `$pip show django-crispy-forms`
2. add the location to the PYTHONPATH as follows:
    `sys.path.append("{location}")`

**Find folders used to look for packages**

I'm not sure what are you trying to do, but if you want to know which folders are used to search for modules being imported you should not rely on PYTHONPATH. Use sys.path for that.

#### Problems and solutions

[Changes in schema not detected by django](https://stackoverflow.com/questions/25958708/django-1-7-no-migrations-to-apply-when-run-migrate-after-makemigrations)



**SECRET_KEY environment variable**

$ export READ_DOT_ENV_FILE=True

**Psycopg2 module not found**
$ PYTHONPATH:

`['', '/Users/Rafa/opt/anaconda3/envs/django/bin', '/Users/Rafa/opt/anaconda3/envs/django/lib/python39.zip', '/Users/Rafa/opt/anaconda3/envs/django/lib/python3.9', '/Users/Rafa/opt/anaconda3/envs/django/lib/python3.9/lib-dynload', '/Users/Rafa/opt/anaconda3/envs/django/lib/python3.9/site-packages', '/Users/Rafa/opt/anaconda3/envs/django/lib/python3.9/site-packages/psycopg2-2.9.1-py3.9-macosx-10.9-x86_64.egg']`

**One liner to get PYTHONPATH in terminal**

python -c "import sys; print('\n'.join(sys.path))"

[Is there any way to change username field label in user authentication login page?](https://stackoverflow.com/questions/53980603/is-there-any-way-to-change-username-field-label-in-user-authentication-login-pag)

**How to make a callback to Google Maps init in separate files of a web app**
[Link](https://stackoverflow.com/questions/38627259/how-to-make-a-callback-to-google-maps-init-in-separate-files-of-a-web-app/38627705 )


**Django Filtering**
[Link](https://www.youtube.com/watch?v=nle3u6Ww6Xk)
[Django Filter library](https://django-filter.readthedocs.io/en/stable/index.html)
[Filter Queryset Dynamically](How to Filter QuerySets Dynamically)



### Activar django env with venv

`source {name-of-venv}/bin/activate`

