# -*- coding: utf-8 -*-
import json

from django.test.testcases import TestCase

from .factories import DishFactory, DishFoodFactory, MealFactory
from foods.tests.factories import FoodFactory
from meals.constant import LUNCH, BREAKFAST, SUPPER
from meals.models import Meal
from meals.tests.factories import MealCategoryFactory


class DishTests(TestCase):
    """
    Tests for model Dish
    """
    def test_get_food_elements(self):
        """
        Check if the total amount of each elemnts are returned
        """
        food = FoodFactory(heat=10)
        dish = DishFactory()
        DishFoodFactory(dish=dish, food=food, weight=100)

        elements = dish.get_food_elements()
        self.assertTrue(elements['weight'] == 100)
        self.assertTrue(elements['heat'] == 10)
        for name in ['carbohydrate', 'fat', 'protein', 'cellulose']:
            self.assertTrue(elements[name] == '-')


class MealCategoryTests(TestCase):
    """
    Tests for MealCategory
    """
    def test_unicode(self):
        """
        Check if the category name is returned
        """
        cat = MealCategoryFactory(name='cat')
        self.assertEqual('cat', str(cat))


class MealTests(TestCase):
    """
    Tests for model Meal
    """
    def test_get_limitations(self):
        """
        Check if the limitations with labels are returned
        """
        meal = MealFactory(limitations='["{}"]'.format(LUNCH))
        self.assertEqual(
            meal.get_limitations(),
            json.dumps([{'type': LUNCH, 'label': Meal.MEAL_TYPES[LUNCH]}]))

    def test_get_limitations_display(self):
        """
        Check if the limitation lables are returned
        """
        meal = MealFactory(limitations='["{}","{}","{}"]'.format(BREAKFAST, LUNCH, SUPPER))  # noqa
        self.assertEqual(meal.get_limitations_display(), u'早餐,午餐,晚餐')

    def test_get_categories_display(self):
        """
        Check if the categories label is returned
        """
        cat1 = MealCategoryFactory(name='cat1')
        cat2 = MealCategoryFactory(name='cat2')
        meal = MealFactory(limitations='["{}"]'.format(LUNCH))
        meal.categories.add(cat1)
        meal.categories.add(cat2)
        self.assertEqual(meal.get_categories_display(), 'cat1,cat2')
