# -*- coding: utf-8 -*-
from django import template
from django.test.testcases import TestCase

from .factories import FoodFactory


class FoodTagsTests(TestCase):
    """
    Tests for custom food tags
    """
    def test_get_food_element_tag(self):
        """
        Check if the food element is returned
        """
        # avoid import circulation
        from meals.tests.factories import DishFactory, DishFoodFactory


        food = FoodFactory(heat=10)
        dish = DishFactory()
        dishfood = DishFoodFactory(dish=dish, food=food, weight=100)

        # heat
        tpl = template.Template(
            '{% load food_tags %}{% get_food_element food "heat" dishfood.weight %}')  # noqa
        rendered = tpl.render(template.Context({'food': food,
                                                'dishfood': dishfood}))
        self.assertEqual(rendered, '10.0')

        # fat
        tpl = template.Template(
            '{% load food_tags %}{% get_food_element food "fat" dishfood.weight %}')  # noqa
        rendered = tpl.render(template.Context({'food': food,
                                                'dishfood': dishfood}))
        self.assertEqual(rendered, '-')
