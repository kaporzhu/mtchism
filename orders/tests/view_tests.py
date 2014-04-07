# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

from django.test.client import RequestFactory
from django.test.testcases import TestCase

import mock

from .factories import OrderFactory
from accounts.tests.factories import UserFactory
from buildings.tests.factories import BuildingFactory
from meals.tests.factories import MealFactory
from orders.constant import CANCELED, DONE
from orders.forms import CheckoutForm
from orders.models import Order
from orders.views import(
    CheckoutView, MyOrderView, CancelOrderView, UpdateOrderStatusView,
    OrderListView
)


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
        building = BuildingFactory()
        form.cleaned_data = {'meals': [{'id': meal.id, 'amount': 1}],
                             'building': building.id, 'location': ''}
        request = RequestFactory()
        request.user = UserFactory()
        view = CheckoutView()
        view.request = request
        response = view.form_valid(form)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertTrue(Order.objects.exists())

    def _fake_get_context_data(self):
        """
        Return empty dict directly
        """
        return {}

    @mock.patch('django.views.generic.edit.FormView.get_context_data',
                _fake_get_context_data)
    def test_get_context_data(self):
        """
        Check if buildings, meal_type_choices and deliver times
        are added to the context
        """
        building = BuildingFactory()
        view = CheckoutView()
        data = view.get_context_data()
        self.assertEqual(
            sorted(data['buildings'].keys()),
            sorted(['buildings', 'meal_type_choices', 'deliver_times']))
        self.assertTrue(building in data['buildings'])


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


class OrderListViewTests(TestCase):
    """
    Tests for OrderListView
    """
    def test_get_params_from_request(self):
        """
        Check the request params are converted
        """
        request = RequestFactory()
        view = OrderListView()
        view.request = request

        # no params in the request
        request.GET = {}
        params = view.get_params_from_request()
        self.assertEqual(params, {'status': 'all', 'building': 'all',
                                  'location': '', 'created_start_dt': None,
                                  'created_end_dt': None})

        # all params in the request
        now = datetime.now()
        now = datetime(now.year, now.month, now.day, now.hour, now.minute)
        request.GET = {'status': DONE, 'building': 'China', 'location': '110',
                       'created-start-datetime': now.strftime('%m/%d/%Y %H:%M'),  # noqa
                       'created-end-datetime': now.strftime('%m/%d/%Y %H:%M')}
        params = view.get_params_from_request()
        self.assertEqual(params, {'status': DONE, 'building': 'China',
                                  'location': '110', 'created_start_dt': now,
                                  'created_end_dt': now})

    def test_get_queryset(self):
        """
        Check if the filtered orders are returned
        """
        request = RequestFactory()
        request.GET = {}
        building = BuildingFactory()
        view = OrderListView()
        view.request = request
        order = OrderFactory(building=building, location='location')

        # without any filter
        qs = view.get_queryset()
        self.assertTrue(qs.filter(id=order.id).exists())

        # status filter
        request.GET = {'status': DONE}
        qs = view.get_queryset()
        self.assertFalse(qs.filter(id=order.id).exists())

        # address building filter
        request.GET = {'building': building.id, 'location': ''}
        qs = view.get_queryset()
        self.assertTrue(qs.filter(id=order.id).exists())

        # address location filter
        request.GET = {'location': '111'}
        qs = view.get_queryset()
        self.assertFalse(qs.filter(id=order.id).exists())
        request.GET = {'location': 'location'}
        qs = view.get_queryset()
        self.assertTrue(qs.filter(id=order.id).exists())

        # start < end
        start = order.created_at - timedelta(days=1)
        end = order.created_at + timedelta(days=1)
        # created time
        # start only
        request.GET = {'created-start-datetime':
                       start.strftime('%m/%d/%Y %H:%M')}
        qs = view.get_queryset()
        self.assertTrue(qs.filter(id=order.id).exists())
        # end only
        request.GET = {'created-end-datetime':
                       end.strftime('%m/%d/%Y %H:%M')}
        qs = view.get_queryset()
        self.assertTrue(qs.filter(id=order.id).exists())
        # start and end
        request.GET = {'created-start-datetime':
                       start.strftime('%m/%d/%Y %H:%M'),
                       'created-end-datetime':
                       end.strftime('%m/%d/%Y %H:%M')}
        qs = view.get_queryset()
        self.assertTrue(qs.filter(id=order.id).exists())

        # start > end
        start = order.created_at + timedelta(days=1)
        end = order.created_at - timedelta(days=1)
        # start only
        request.GET = {'created-start-datetime':
                       start.strftime('%m/%d/%Y %H:%M')}
        qs = view.get_queryset()
        self.assertFalse(qs.filter(id=order.id).exists())
        # end only
        request.GET = {'created-end-datetime':
                       end.strftime('%m/%d/%Y %H:%M')}
        qs = view.get_queryset()
        self.assertFalse(qs.filter(id=order.id).exists())
        # start and end
        request.GET = {'created-start-datetime':
                       start.strftime('%m/%d/%Y %H:%M'),
                       'created-end-datetime':
                       end.strftime('%m/%d/%Y %H:%M')}
        qs = view.get_queryset()
        self.assertFalse(qs.filter(id=order.id).exists())

    def _fake_get_context_data(self, **kwargs):
        """
        Fake get_context_data, return empty dict directly
        """
        return {}

    @mock.patch('django.views.generic.list.ListView.get_context_data',
                _fake_get_context_data)
    def test_get_context_data(self):
        """
        Check if the status_choices and request params are added to the context
        """
        request = RequestFactory()
        request.GET = {}
        view = OrderListView()
        view.request = request
        self.assertEqual(sorted(view.get_context_data().keys()),
                         sorted(['status_choices', 'status', 'building',
                                 'buildings', 'location', 'created_start_dt',
                                 'created_end_dt']))


class UpdateOrderStatusViewTests(TestCase):
    """
    Tests for UpdateOrderStatusView
    """
    def test_get_ajax(self):
        """
        Check if the order status is updated
        """
        order = OrderFactory()
        request = RequestFactory()
        request.GET = {'status': DONE, 'ids': str(order.id)}
        view = UpdateOrderStatusView()
        response = view.get_ajax(request)
        self.assertTrue(json.loads(response.content)['success'] == True)
        self.assertTrue(Order.objects.get(pk=order.id).status == DONE)
