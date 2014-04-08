# -*- coding: utf-8 -*-
import os
import platform

from fabric.api import local

from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mtchism.settings")


def test():
    """
    Run the tests with trial
    """
    for app in settings.LOCAL_APPS:
        local('python manage.py test %s.tests' % app)


def coverage():
    """
    Check tests coverage
    """
    apps = ' '.join(['%s.tests' % app for app in settings.LOCAL_APPS])
    local('coverage run --source=. manage.py test %s' % apps)
    local('coverage report')
    local('coverage html')
    if platform.system().lower() == 'windows':
        local(os.path.join('htmlcov', 'index.html'))
    else:
        local(os.path.join('htmlcov', 'index.html'))


def flake8():
    """
    PEP8 check
    """
    local('flake8 . --statistics --exclude="migrations,doc"')
