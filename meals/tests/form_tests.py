# -*- coding: utf-8 -*-
from django import forms
from django.test.testcases import TestCase

from meals.forms import UpdateDishFoodsForm


class UpdateDishFoodsFormTests(TestCase):
    """
    Tests for UpdateDishFoodsForm
    """
    def test_clean_foods(self):
        """
        Check if the foods is converted to JSON
        """
        form = UpdateDishFoodsForm()

        # valid data
        form.data = {'foods': '{}'}
        self.assertTrue(form.clean_foods() == {})

        # invalid data
        form.data = {'foods': 'test'}
        self.assertRaises(forms.ValidationError, lambda: form.clean_foods())
