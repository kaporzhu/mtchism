# -*- coding: utf-8 -*-
from django.test.testcases import TestCase

from .factories import CategoryFactory, FoodFactory


class CategoryTests(TestCase):
    """
    Tests for Category model
    """
    def test_unicode(self):
        category = CategoryFactory()
        self.assertEqual(str(category), category.name)


class FoodTests(TestCase):
    """
    Tests for Food model
    """
    def test_unicode(self):
        food = FoodFactory()
        self.assertEqual(str(food), food.name)
