# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import CheckoutView, MyOrderView


urlpatterns = patterns(
    '',
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^mine/$', MyOrderView.as_view(), name='mine'),
)
