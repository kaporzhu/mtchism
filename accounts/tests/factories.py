# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

import factory


class UserFactory(factory.DjangoModelFactory):
    """
    Factory for User
    """
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: str(10000000000+n))
    first_name = 'test_first_name'
    last_name = 'test_last_name'
