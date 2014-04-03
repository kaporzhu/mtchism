# -*- coding: utf-8 -*-
import factory

from accounts.tests.factories import UserFactory
from foods.tests.factories import FoodFactory
from meals.models import Dish, DishFood, Meal


class DishFactory(factory.DjangoModelFactory):
    """
    Factory for Dish
    """
    FACTORY_FOR = Dish

    creator = factory.SubFactory(UserFactory)
    name = 'I am a dish'


class DishFoodFactory(factory.DjangoModelFactory):
    """
    Factory for DishFood
    """
    FACTORY_FOR = DishFood

    dish = factory.SubFactory(DishFactory)
    food = factory.SubFactory(FoodFactory)
    creator = factory.SubFactory(UserFactory)
    weight = 100


class MealFactory(factory.DjangoModelFactory):
    """
    Factory for Meal
    """
    FACTORY_FOR = Meal

    creator = factory.SubFactory(UserFactory)
    name = 'I am a meal'
