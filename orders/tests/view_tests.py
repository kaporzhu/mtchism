# -*- coding: utf-8 -*-
import json

from django.test.client import RequestFactory
from django.test.testcases import TestCase

from accounts.tests.factories import UserFactory
from meals.tests.factories import MealFactory
from orders.forms import CheckoutForm
from orders.views import CheckoutView
from orders.models import Order


class CheckoutViewTests(TestCase):
    """
    Tests for CheckoutView
    """

    def test_form_valid(self):
        """
        Check if the new order is created
        """
        form = CheckoutForm()
        meal = MealFactory()
        form.cleaned_data = {'meals': [{'id': meal.id, 'amount': 1}],
                             'address': 'address'}
        request = RequestFactory()
        request.user = UserFactory()
        view = CheckoutView()
        view.request = request
        response = view.form_valid(form)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertTrue(Order.objects.exists())
