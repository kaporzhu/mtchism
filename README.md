mtchism
=======

Online meal ordering system


How to set up the dev env?
==========================

    $ pip install virtualenv virtualenvwrapper
    $ mkvirtualenv mtchism
    $ workon mtchism
    (mtchism)$ pip install -r dev-requirements.txt
    (mtchism)$ cp local_settings.py.sample local_settings.py
    (mtchism)$ python manage.py syncdb
    (mtchism)$ python manage.py migrate
    (mtchism)$ python manage.py runserver

How to run the tests?
=====================

    $ workon mtchism
    (mtchism)$ fab test
    (mtchism)$ fab coverage
    (mtchism)$ fab flake8


More doc?
=========
I don't have much to create the sphinx doc.
But I will create a simple one later.
