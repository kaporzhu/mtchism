# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from foods.models import Category, Food
from meals.models import Dish, DishFood


class FoodTagsTests(TestCase):
    """
    Tests for custom food tags
    """
    def test_get_food_element_tag(self):
        """
        Check if the food element is returned
        """
        category, created = Category.objects.get_or_create(name='cat')
        food, created = Food.objects.get_or_create(name='food',
                                                   category=category, heat=10)
        user, created = User.objects.get_or_create(username='test')
        dish, created = Dish.objects.get_or_create(name='dish', creator=user)
        dishfood, created = DishFood.objects.get_or_create(
            creator=user, dish=dish, food=food, weight=100)

        # heat
        tpl = template.Template(
            '{% load food_tags %}{% get_food_element food "heat" dishfood.weight %}')  # noqa
        rendered = tpl.render(template.Context({'food': food, 'dishfood': dishfood}))
        self.assertEqual(rendered, '10.0')

        # fat
        tpl = template.Template(
            '{% load food_tags %}{% get_food_element food "fat" dishfood.weight %}')  # noqa
        rendered = tpl.render(template.Context({'food': food, 'dishfood': dishfood}))
        self.assertEqual(rendered, '-')
