# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Dish, DishFood, Meal


admin.site.register(Dish)
admin.site.register(DishFood)
admin.site.register(Meal)
