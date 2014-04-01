# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import UploadFoodView


urlpatterns = patterns(
    '',
    url(r'^upload/$', UploadFoodView.as_view(), name='upload'),
)
