# -*- coding: utf-8 -*-
from django import forms
from django.test.testcases import TestCase

from .factories import UserFactory
from .mixins import AccountTestMixin
from accounts.forms import LoginForm, RegisterForm


class LoginFormTests(AccountTestMixin, TestCase):
    """
    Tests for LoginForm
    """
    def test_clean(self):
        """
        Raise ValidationError if username or password doesn't match
        """
        # add test User account
        user = UserFactory()
        user.set_password('123')
        user.save()

        # incorrect username
        data = {'username': 'fake_user', 'password': '123'}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

        # incorrect password
        data = {'username': user.username, 'password': 'fake_password'}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

        # valid account
        data = {'username': user.username, 'password': '123'}
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
        user = UserFactory()
        form.data = {'username': user.username}
        self.assertRaises(forms.ValidationError, lambda: form.clean())

        # new phone
        form.data = {'username': '12345678911'}
        self.assertTrue('username' in form.clean())
