# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import UploadFoodView, SearchFoodView


urlpatterns = patterns(
    '',
    url(r'^upload/$', UploadFoodView.as_view(), name='upload'),
    url(r'^search/$', SearchFoodView.as_view(), name='search'),
)
