# -*- coding: utf-8 -*-
import factory

from buildings.models import Building, Tag


class BuildingFactory(factory.DjangoModelFactory):
    """
    Factory for food Building
    """
    FACTORY_FOR = Building


class TagFactory(factory.DjangoModelFactory):
    """
    Factory for Tag
    """
    FACTORY_FOR = Tag
