# -*- coding: utf-8 -*-
from django.http.request import QueryDict
from django.test.client import RequestFactory
from django.test.testcases import TestCase
from django.views.generic.base import TemplateView

from mtchism.mixins import PaginationMixin


class PaginationMixinTests(TestCase):
    """
    Tests for PaginationMixin
    """
    def test_get_context_data(self):
        """
        Check if the page param is removed and query string is returned
        """
        class TestView(PaginationMixin, TemplateView):
            pass
        request = RequestFactory()
        request.GET = QueryDict('page=1&name=kapor')
        view = TestView()
        view.request = request
        data = view.get_context_data()
        self.assertIn('query_string', data)
        self.assertNotIn('page', data['query_string'])
        self.assertIn('name', data['query_string'])
