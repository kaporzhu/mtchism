How to set up the project
=========================


.. topic:: Overview

    Here are the steps for setting up the project

Steps
-----

1. Install virtualenv.

.. code-block:: console

    $ pip install virtualenv virtualenvwrapper
    $ mkvirtualenv mtchism

2. Install the requirements.

.. code-block:: console

    $ workon mtchism
    (mtchism)$ pip install -r requirements.txt


3. Update the database configuration in `mtchism/mtchism/settings.py`.

    If you are working on local, copy `mtchism/mtchism/local_settings.py.sample`
   to `mtchism/mtchism/local_settings.py`. Update the settings for local only.


4. Create database.
   If you are using mysql:
.. code-block:: console

    (mtchism)$ mysql> create database mtchism default charset='utf8';


5. Create the tables with Django command.

.. code-block:: console

    (mtchism)$ python manage.py syncdb
    (mtchism)$ python manage.py migrate

.. attention:: 

    If you don't want to the South, simply commnet *south* in the
    settings.py:INSTALLED_APPS and do **python manage.py syncdb** only.


6. Start the service

.. code-block:: console

    (mtchism)$ python manage.py runserver

5. Access `http://127.0.0.1:8000/`.
