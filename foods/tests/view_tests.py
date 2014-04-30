# -*- coding: utf-8 -*-
import json

from django.db.models.query import QuerySet
from django.test.client import RequestFactory
from django.test.testcases import TestCase

from .factories import FoodFactory
from foods.views import SearchFoodView


class SearchFoodViewTests(TestCase):
    """
    Tests for SearchFoodView
    """
    def test_search(self):
        """
        Check if the foods is returned
        """
        view = SearchFoodView()
        self.assertTrue(isinstance(view.search('Test'), QuerySet))

    def _fake_render_json_response(self, context_dict):
        """
        Fake render_json_response, return context_dict directly
        """
        return context_dict

    def test_get_ajax(self):
        """
        Check if the foods is returned in JSON
        """
        food = FoodFactory()
        request = RequestFactory()
        request.GET = {'term': food.name}
        view = SearchFoodView()
        response = view.get_ajax(request)
        foods = json.loads(response.content)
        self.assertTrue(len(foods) == 1)
