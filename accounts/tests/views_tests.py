# -*- coding: utf-8 -*-
from django.contrib import auth
from django.test.testcases import TestCase

from .mixins import AccountTestMixin
from accounts.forms import LoginForm
from accounts.views import LoginView, LogoutView


class LoginViewTests(AccountTestMixin, TestCase):
    """
    Tests for LoginView
    """
    def test_form_valid(self):
        """
        Check if the user is authenticated.
        """
        # add test User account
        self.create_user('test', '123')

        # create LoginView
        view = LoginView()
        view.request = self.generate_request()

        # create LoginForm
        form = LoginForm()
        form.data = {'username': 'test',
                     'password': '123'}
        form.cleaned_data = form.clean()

        # test now
        view.form_valid(form)
        self.assertEqual(view.request.user.username, 'test')
        self.assertTrue(view.request.user.is_authenticated())


class LogoutViewTests(AccountTestMixin, TestCase):
    """
    Tests for LogoutView
    """

    def test_get(self):
        """
        Check if authenticated user is logged out
        """
        # create test User account
        self.create_user('test', '123')

        # create LogoutView
        view = LogoutView()
        view.request = self.generate_request()

        # test now
        user = auth.authenticate(username='test', password='123')
        auth.login(view.request, user)
        self.assertTrue(view.request.user.is_authenticated())
        view.get(view.request)
        self.assertFalse(view.request.user.is_authenticated())
