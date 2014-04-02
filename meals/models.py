# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from foods.models import Food


class Dish(models.Model):
    """
    Each meal has several dishes
    """
    name = models.CharField(max_length=256)

    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)


class DishFood(models.Model):
    """
    Foods in a dish
    """
    dish = models.ForeignKey(Dish)
    food = models.ForeignKey(Food)
    weight = models.FloatField()  # gram

    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)


class Meal(models.Model):
    """
    Each meal in a day.
    """
    name = models.CharField(max_length=128)
    dishes = models.ManyToManyField(Dish)

    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
