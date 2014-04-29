# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Tag, Building


admin.site.register(Tag)
admin.site.register(Building)
