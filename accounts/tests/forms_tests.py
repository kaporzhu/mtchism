# -*- coding: utf-8 -*-
from django.test.testcases import TestCase

from .mixins import AccountTestMixin
from accounts.forms import LoginForm, RegisterForm
from django import forms


class LoginFormTests(AccountTestMixin, TestCase):
    """
    Tests for LoginForm
    """
    def test_clean(self):
        """
        Raise ValidationError if username or password doesn't match
        """
        # add test User account
        self.create_user('12345678900', '123')

        # incorrect username
        data = {'username': 'fake_user', 'password': '123'}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

        # incorrect password
        data = {'username': '12345678900', 'password': 'fake_password'}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

        # valid account
        data = {'username': '12345678900', 'password': '123'}
        form = LoginForm(data)
        self.assertTrue(form.is_valid())


class RegisterFormTests(AccountTestMixin, TestCase):
    """
    Tests for RegisterForm
    """

    def test_clean(self):
        """
        1. phone is already existed.
        2. phone is new.
        """
        form = RegisterForm()

        # phone exists
        self.create_user('12345678900', '123')
        form.data = {'username': '12345678900'}
        self.assertRaises(forms.ValidationError, lambda: form.clean())

        # new phone
        form.data = {'username': '12345678911'}
        self.assertTrue('username' in form.clean())
