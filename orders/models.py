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

    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default=CREATED)
    total_price = models.FloatField(default=0)
    total_amount = models.IntegerField(default=0)
    address = models.CharField(max_length=256, blank=True)
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderMeal(models.Model):
    """
    Meal for order
    """
    meal = models.ForeignKey(Meal)
    order = models.ForeignKey(Order)
    amount = models.IntegerField()
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
