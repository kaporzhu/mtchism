# -*- coding: utf-8 -*-
from django.test.client import RequestFactory
from django.test.testcases import TestCase

import mock

from .factories import TagFactory
from buildings.views import BuildingListView
from buildings.tests.factories import BuildingFactory


class BuildingListViewTests(TestCase):
    """
    tests for BuildingListView
    """

    def _fake_get_context_data(self):
        """
        Fake get_context_data, return empty dict directly
        """
        return {}

    @mock.patch('django.views.generic.list.ListView.get_context_data',
                _fake_get_context_data)
    def test_get_context_data(self):
        """
        Check if the tags and request GET params are added to the conext
        """
        request = RequestFactory()
        request.GET = {'name': 'value'}
        view = BuildingListView()
        view.request = request
        data = view.get_context_data()
        self.assertTrue('tags' in data)
        self.assertTrue(data['name'] == 'value')

    def test_get_queryset(self):
        """
        Check if the building are filtered by tag
        """
        tag = TagFactory()
        building = BuildingFactory()
        building.tags.add(tag)
        request = RequestFactory()
        request.GET = {'tag': 'all'}
        view = BuildingListView()
        view.request = request
        self.assertTrue(building in view.get_queryset())
        request.GET = {'tag': 'tag'}
        self.assertFalse(view.get_queryset().exists())
