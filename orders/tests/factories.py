# -*- coding: utf-8 -*-
from datetime import datetime

import factory

from accounts.tests.factories import UserFactory
from meals.tests.factories import MealFactory
from orders.models import OrderMeal, Order


class OrderFactory(factory.DjangoModelFactory):
    """
    Factory for Order
    """
    FACTORY_FOR = Order

    creator = factory.SubFactory(UserFactory)
    deliver_date = datetime.now().date()


class OrderMealFactory(factory.DjangoModelFactory):
    """
    Factory for User
    """
    FACTORY_FOR = OrderMeal

    creator = factory.SubFactory(UserFactory)
    order = factory.SubFactory(OrderFactory)
    meal = factory.SubFactory(MealFactory)
    amount = 0
