# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Order, OrderMeal


admin.site.register(Order)
admin.site.register(OrderMeal)
