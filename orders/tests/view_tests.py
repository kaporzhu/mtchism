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
from orders.constant import CANCELED, DONE, LUNCH, DELIVER_TIMES, BREAKFAST
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
                             'building': building.id, 'location': '',
                             'meal_type': LUNCH, 'deliver_time': '11:00-12:00'}
        request = RequestFactory()
        request.user = UserFactory()
        view = CheckoutView()
        view.request = request
        response = view.form_valid(form)
        self.assertTrue(json.loads(response.content)['success'])
        order = Order.objects.get(building=building)
        self.assertTrue(order.meal_type == form.cleaned_data['meal_type'])
        self.assertTrue(order.deliver_time == form.cleaned_data['deliver_time'])  # noqa
        self.assertTrue(order.location == form.cleaned_data['location'])
        self.assertTrue(getattr(order.creator.profile, 'preferred_{}_time'.format(LUNCH)) == form.cleaned_data['deliver_time'])  # noqa
        self.assertTrue(order.ordermeal_set.filter(meal=meal).exists())

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
            sorted(data.keys()),
            sorted(['buildings', 'meal_type_choices', 'deliver_times', 'tomorrow']))  # noqa
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
        order_today = OrderFactory(creator=user)
        order_tomorrow = OrderFactory(creator=user)
        order_tomorrow.deliver_date = datetime.now() + timedelta(days=1)
        order_tomorrow.save()
        order_yesterday = OrderFactory(creator=user)
        order_yesterday.deliver_date = datetime.now() - timedelta(days=1)
        order_yesterday.save()
        order_older = OrderFactory(creator=user)
        order_older.deliver_date = datetime.now() - timedelta(days=2)
        order_older.save()
        request = RequestFactory()
        request.user = user
        view = MyOrderView()
        view.request = request
        data = view.get_context_data()
        self.assertEqual(sorted(['tomorrow', 'today', 'yesterday']),
                         sorted(data['my_orders']))
        self.assertIn(order_today, data['my_orders']['today'])
        self.assertIn(order_tomorrow, data['my_orders']['tomorrow'])
        self.assertIn(order_yesterday, data['my_orders']['yesterday'])


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
                                  'created_end_dt': None, 'meal_type': 'all',
                                  'deliver_time': 'all'})

        # all params in the request
        now = datetime.now()
        now = datetime(now.year, now.month, now.day, now.hour, now.minute)
        request.GET = {'status': DONE, 'building': 'China', 'location': '110',
                       'created-start-datetime': now.strftime('%m/%d/%Y %H:%M'),  # noqa
                       'created-end-datetime': now.strftime('%m/%d/%Y %H:%M'),
                       'meal-type': LUNCH, 'deliver-time': '11:00-12:00'}
        params = view.get_params_from_request()
        self.assertEqual(params, {'status': DONE, 'building': 'China',
                                  'location': '110', 'created_start_dt': now,
                                  'created_end_dt': now, 'meal_type': LUNCH,
                                  'deliver_time': '11:00-12:00'})

    def test_get_queryset(self):
        """
        Check if the filtered orders are returned
        """
        request = RequestFactory()
        request.GET = {}
        building = BuildingFactory()
        view = OrderListView()
        view.request = request
        order = OrderFactory(building=building, location='location',
                             meal_type=LUNCH,
                             deliver_time=DELIVER_TIMES[LUNCH][0])

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

        # meal type
        request.GET = {'meal-type': BREAKFAST}
        qs = view.get_queryset()
        self.assertFalse(qs.filter(id=order.id).exists())
        request.GET = {'meal-type': LUNCH}
        qs = view.get_queryset()
        self.assertTrue(qs.filter(id=order.id).exists())

        # deliver time
        request.GET = {'deliver-time': DELIVER_TIMES[BREAKFAST][0]}
        qs = view.get_queryset()
        self.assertFalse(qs.filter(id=order.id).exists())
        request.GET = {'deliver-time': DELIVER_TIMES[LUNCH][0]}
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
                                 'created_end_dt', 'deliver_times',
                                 'deliver_time', 'meal_type_choices',
                                 'meal_type']))


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
        self.assertTrue(json.loads(response.content)['success'])
        self.assertTrue(Order.objects.get(pk=order.id).status == DONE)
