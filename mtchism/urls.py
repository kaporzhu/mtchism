from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('portals.urls', 'portals', 'portals')),
    url(r'^accounts/', include('accounts.urls', 'accounts', 'accounts')),
    url(r'^foods/', include('foods.urls', 'foods', 'foods')),
    url(r'^meals/', include('meals.urls', 'meals', 'meals')),
    url(r'^orders/', include('orders.urls', 'orders', 'orders')),

    url(r'^admin/', include(admin.site.urls)),
)
