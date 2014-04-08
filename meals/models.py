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

    def get_food_elements(self):
        """
        Get total nutrient elements
        """
        elements = {}
        total_weight = 0
        names = ['heat', 'carbohydrate', 'fat', 'protein', 'cellulose']
        for dishfood in self.dishfood_set.all():
            total_weight += dishfood.weight
            for name in names:
                amount = elements.get(name, 0)
                food = dishfood.food
                if getattr(food, name) != -1:
                    amount += getattr(food, name)/100.0*dishfood.weight
                    elements[name] = amount

        # add total weight
        elements['weight'] = total_weight

        # set default value if doesn't exist
        for name in names:
            if name not in elements:
                elements[name] = '-'

        return elements


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
    price = models.FloatField(default=0)
    # breakfast, lunch, supper. Seperate with comma
    limitations = models.CharField(max_length=32, blank=True)

    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
