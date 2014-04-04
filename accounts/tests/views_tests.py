# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from .factories import UserFactory
from .mixins import AccountTestMixin
from accounts.forms import LoginForm, RegisterForm
from accounts.views import LoginView, LogoutView, RegisterView


class LoginViewTests(AccountTestMixin, TestCase):
    """
    Tests for LoginView
    """
    def test_form_valid(self):
        """
        Check if the user is authenticated.
        """
        # add test User account
        user = UserFactory()
        user.set_password('123')
        user.save()

        # create LoginView
        view = LoginView()
        view.request = self.generate_request()

        # create LoginForm
        form = LoginForm()
        form.data = {'username': user.username,
                     'password': '123'}
        form.cleaned_data = form.clean()

        # test now
        view.form_valid(form)
        self.assertEqual(view.request.user.username, user.username)
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
        user = UserFactory()
        user.set_password('123')
        user.save()

        # create LogoutView
        view = LogoutView()
        view.request = self.generate_request()

        # test now
        user = auth.authenticate(username=user.username, password='123')
        auth.login(view.request, user)
        self.assertTrue(view.request.user.is_authenticated())
        view.get(view.request)
        self.assertFalse(view.request.user.is_authenticated())


class RegisterViewTests(TestCase):
    """
    Tests for RegisterView
    """
    def test_form_valid(self):
        """
        Check if the new user object is created
        """
        view = RegisterView()
        form = RegisterForm()
        form.cleaned_data = {'username': '12345678912', 'password': '123'}
        view.form_valid(form)
        self.assertTrue(User.objects.filter(username='12345678912').exists())
