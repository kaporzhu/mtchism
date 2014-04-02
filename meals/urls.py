# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import CreateMealView, UpdateMealView, MealListView


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateMealView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', UpdateMealView.as_view(), name='update'),
    url(r'^list/$', MealListView.as_view(), name='list'),
)
