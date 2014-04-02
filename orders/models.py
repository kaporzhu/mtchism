# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from .constant import CREATED, PAID, DONE, CANCELED
from meals.models import Meal


class Order(models.Model):
    """
    Model for order
    """

    STATUS_CHOICES = (
        (CREATED, 'created'),
        (PAID, 'paid'),
        (DONE, 'done'),
        (CANCELED, 'canceled'),
    )

    meals = models.ManyToManyField(Meal)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default=CREATED)
    total_price = models.FloatField()
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
