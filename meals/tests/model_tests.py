# -*- coding: utf-8 -*-
from django.test.testcases import TestCase

from .factories import DishFactory, DishFoodFactory
from foods.tests.factories import FoodFactory


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
