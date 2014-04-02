# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateMealView, UpdateMealView, MealListView,
    CreateDishView, UpdateDishView, UpdateDishFoodsView
)


urlpatterns = patterns(
    '',
    # meal
    url(r'^create/$', CreateMealView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', UpdateMealView.as_view(), name='update'),
    url(r'^list/$', MealListView.as_view(), name='list'),

    # dish
    url(r'^(?P<meal_pk>\d+)/dishes/create/$',
        CreateDishView.as_view(), name='create_dish'),
    url(r'^(?P<meal_pk>\d+)/dishes/update/(?P<pk>\d+)/$',
        UpdateDishView.as_view(), name='update_dish'),

    # dish foods
    url(r'^(?P<meal_pk>\d+)/dishes/(?P<dish_pk>\d+)/foods/update/$',
        UpdateDishFoodsView.as_view(), name='update_dish_foods'),
)
