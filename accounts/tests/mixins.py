# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
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
