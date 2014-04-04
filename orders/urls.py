# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import CheckoutView


urlpatterns = patterns(
    '',
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
)
