# -*- coding: utf-8 -*-
import factory

from foods.models import Category, Food


class CategoryFactory(factory.DjangoModelFactory):
    """
    Factory for food Category
    """
    FACTORY_FOR = Category

    name = 'I am food category'


class FoodFactory(factory.DjangoModelFactory):
    """
    Factory for Food
    """
    FACTORY_FOR = Food

    category = factory.SubFactory(CategoryFactory)
    name = 'I am food'
