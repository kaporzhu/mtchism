# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Category, Food


admin.site.register(Category)
admin.site.register(Food)
