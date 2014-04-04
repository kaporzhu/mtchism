# -*- coding: utf-8 -*-
import json

from django.test.client import RequestFactory
from django.test.testcases import TestCase

import mock

from .factories import OrderFactory
from accounts.tests.factories import UserFactory
from meals.tests.factories import MealFactory
from orders.constant import CANCELED
from orders.forms import CheckoutForm
from orders.models import Order
from orders.views import CheckoutView, MyOrderView, CancelOrderView


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


class MyOrderViewTests(TestCase):
    """
    Tests for MyOrderView
    """

    def _fake_get_context_data(self):
        """
        Return empty dict directly
        """
        return {}

    @mock.patch('django.views.generic.base.TemplateView.get_context_data',
                _fake_get_context_data)
    def test_get_context_data(self):
        """
        Check if my orders are added to the context
        """
        user = UserFactory()
        order = OrderFactory(creator=user)
        request = RequestFactory()
        request.user = user
        view = MyOrderView()
        view.request = request
        data = view.get_context_data()
        self.assertIn(order, data['orders'])


class CancelOrderViewTests(TestCase):
    """
    Tests for CancelOrderView
    """
    def test_get(self):
        """
        Check if the order status is changed
        """
        creator = UserFactory()
        someone = UserFactory()
        order = OrderFactory(creator=creator)
        request = RequestFactory()
        view = CancelOrderView()
        view.request = request

        # creator try to cancel the order
        request.user = creator
        view.get(None, pk=order.id)
        order = Order.objects.get(pk=order.id)
        self.assertEqual(order.status, CANCELED)

        # someone try to cancel the order
        request.user = someone
        self.assertRaises(Order.DoesNotExist, lambda: view.get(None, pk=order.id))  # noqa
