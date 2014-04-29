# -*- coding: utf-8 -*-
from django.test.testcases import TestCase

from .factories import OrderFactory
from orders.constant import CREATED, PAID
from orders.models import Order
from orders.tests.factories import OrderMealFactory


class OrderTests(TestCase):
    """
    Tests for order model
    """
    def test_get_operation_buttons(self):
        """
        Check the operation buttons depends on order status
        """
        # status CREATED
        order = OrderFactory(status=CREATED)
        buttons = order.get_operation_buttons()
        self.assertTrue('取消订单' in buttons)
        self.assertTrue('马上支付' in buttons)

        # status PAID
        order.status = PAID
        buttons = order.get_operation_buttons()
        self.assertIsNone(buttons)

    def test_get_status_label(self):
        """
        Check if the status label is returned
        """
        self.assertEqual(u'等待付款', Order.get_status_label(CREATED))
        self.assertRaises(ValueError, lambda: Order.get_status_label('!!!'))

    def test_unicode(self):
        order = OrderFactory()
        self.assertEqual(
            str(order),
            u'{}-{}'.format(order.building, order.creator.username))


class OrderMealTests(TestCase):
    """
    Tests for OrderMeal model
    """
    def test_unicode(self):
        order_meal = OrderMealFactory()
        self.assertEqual(
            str(order_meal),
            u'{}-{}'.format(order_meal.order, order_meal.meal.name))
