# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import SearchFoodView


urlpatterns = patterns(
    '',
    url(r'^search/$', SearchFoodView.as_view(), name='search'),
)
