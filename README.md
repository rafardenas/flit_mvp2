# Flit MVP 2

First version of Flit that actually solves the trust problem 

We can use the admin page of the site to update Flit "in the back". 



### Resources, problems, solutions

#### Resources

[Make Queries](https://docs.djangoproject.com/en/3.2/topics/db/queries/)

- Query for all recors in database *"Car"*
    - Car.objects.all()
- Filters (*make is a field in the table*)
    - Car.objects.filter(make=Audi)


**django shell**
$ python3 manage.py shell

**create superuser**
$ python3 manage.py createsuperuser

**query all (returns a QuerySet object)**
{table-name}.objects.all()

**Restrict access to a view for no-logged in users**
add the parent-class `LoginRequiredMixin` to the view classes.

**Use signals to trigger routines when a specific event takes place**



#### Problems and solutions

[Changes in schema not detected by django](https://stackoverflow.com/questions/25958708/django-1-7-no-migrations-to-apply-when-run-migrate-after-makemigrations)

