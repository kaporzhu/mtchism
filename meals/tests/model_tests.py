# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from foods.models import Category, Food
from meals.models import Dish, DishFood


class DishTests(TestCase):
    """
    Tests for model Dish
    """
    def test_get_food_elements(self):
        """
        Check if the total amount of each elemnts are returned
        """
        category, created = Category.objects.get_or_create(name='cat')
        food, created = Food.objects.get_or_create(
            name='food', category=category, heat=10)
        user, created = User.objects.get_or_create(username='test')
        dish, created = Dish.objects.get_or_create(name='dish', creator=user)
        DishFood.objects.get_or_create(creator=user, dish=dish, food=food,
                                       weight=100)

        elements = dish.get_food_elements()
        self.assertTrue(elements['weight'] == 100)
        self.assertTrue(elements['heat'] == 10)
        for name in ['carbohydrate', 'fat', 'protein', 'cellulose']:
            self.assertTrue(elements[name] == '-')
