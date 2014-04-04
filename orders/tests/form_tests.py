# -*- coding: utf-8 -*-
from django import forms
from django.test.testcases import TestCase

from orders.forms import CheckoutForm


class CheckoutFormTests(TestCase):
    """
    Tests for CheckoutForm
    """

    def test_clean_meals(self):
        """
        Check if the meals is converted to JSON object
        """
        form = CheckoutForm()

        # invalid json
        form.data = {'meals': 'test'}
        self.assertRaises(forms.ValidationError, lambda: form.clean_meals())

        # valid json
        form.data = {'meals': '[]'}
        self.assertEqual(form.clean_meals(), [])
