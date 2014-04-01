# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory


class AccountTestMixin(object):
    """
    Mixin for Accounts tests
    """
    def generate_request(self):
        """
        Create http request
        """
        request = RequestFactory()
        request.COOKIES = {}
        request.META = {}
        request.user = AnonymousUser()
        SessionMiddleware().process_request(request)
        return request

    def create_user(self, username, password):
        """
        Create a new User object
        """
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()
        return user
