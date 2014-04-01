from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^foods/', include('foods.urls', 'foods', 'foods')),

    url(r'^admin/', include(admin.site.urls)),
)
