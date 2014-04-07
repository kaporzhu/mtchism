# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateBuildingView, UpdateBuildingView, BuildingListView
)


urlpatterns = patterns(
    '',
    url(r'^list/$', BuildingListView.as_view(), name='list'),
    url(r'^create/$', CreateBuildingView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/update/$', UpdateBuildingView.as_view(), name='update'),
)
