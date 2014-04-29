# -*- coding: utf-8 -*-
import os
import platform

from django.conf import settings

from fabric.api import local


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mtchism.settings")


def test(app=None, test=None):
    """
    Run the tests with trial
    """
    if app and test:
        local('python manage.py test {}.tests.{} '
              '--settings=mtchism.test_settings'.format(app, test))
    elif app:
        local('python manage.py test {}.tests '
              '--settings=mtchism.test_settings'.format(app))
    else:
        for app in settings.LOCAL_APPS:
            local('python manage.py test {}.tests '
                  '--settings=mtchism.test_settings'.format(app))


def coverage():
    """
    Check tests coverage
    """
    apps = ' '.join(['%s.tests' % app for app in settings.LOCAL_APPS])
    local('coverage run --source=. manage.py test '
          '--settings=mtchism.test_settings {}'.format(apps))
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
