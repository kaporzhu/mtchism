# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Dish, DishFood, MealCategory, Meal


admin.site.register(Dish)
admin.site.register(DishFood)
admin.site.register(MealCategory)
admin.site.register(Meal)
