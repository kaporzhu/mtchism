# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CheckoutView, MyOrderView, CreateSuccessView, CancelOrderView
)


urlpatterns = patterns(
    '',
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^(?P<pk>\d+)/success/$', CreateSuccessView.as_view(),
        name='success'),
    url(r'^(?P<pk>\d+)/cancel/$', CancelOrderView.as_view(), name='cancel'),
    url(r'^mine/$', MyOrderView.as_view(), name='mine'),
)
