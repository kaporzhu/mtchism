# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from .mixins import AccountTestMixin
from accounts.forms import LoginForm


class LoginFormTests(AccountTestMixin, TestCase):
    """
    Tests for LoginForm
    """
    def test_clean(self):
        """
        Raise ValidationError if username or password doesn't match
        """
        # add test User account
        self.create_user('test', '123')

        # incorrect username
        data = {'username': 'fake_user', 'password': '123'}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

        # incorrect password
        data = {'username': 'test', 'password': 'fake_password'}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

        # valid account
        data = {'username': 'test', 'password': '123'}
        form = LoginForm(data)
        self.assertTrue(form.is_valid())
