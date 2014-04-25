# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreatePlanView, UpdatePlanView, PlanListView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreatePlanView.as_view(), name='create'),
    url(r'^list/$', PlanListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/update/$', UpdatePlanView.as_view(), name='update')
)
