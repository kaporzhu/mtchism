# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreatePlanView, UpdatePlanView, PlanListView, CreateStageView,
    UpdateStageView, IndexView, JoinPlanView, CreateMealView, UpdateMealView,
    MealListView, UserPlanDetailView, StartUserPlanView, BookingView,
    AddWeightView
)


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/$', CreatePlanView.as_view(), name='create'),
    url(r'^list/$', PlanListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/update/$', UpdatePlanView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/join/$', JoinPlanView.as_view(), name='join'),
    url(r'^(?P<plan_pk>\d+)/stages/create/$',
        CreateStageView.as_view(), name='create_stage'),
    url(r'^(?P<plan_pk>\d+)/stages/(?P<pk>\d+)/update/$',
        UpdateStageView.as_view(), name='update_stage'),
    url(r'^(?P<plan_pk>\d+)/stages/(?P<stage_pk>\d+)/meals/create/$',
        CreateMealView.as_view(), name='create_meal'),
    url(r'^(?P<plan_pk>\d+)/stages/(?P<stage_pk>\d+)/meals/list/$',
        MealListView.as_view(), name='meal_list'),
    url(r'^(?P<plan_pk>\d+)/stages/(?P<stage_pk>\d+)/meals/(?P<pk>\d+)/update/$',  # noqa
        UpdateMealView.as_view(), name='update_meal'),
    url(r'^userplans/(?P<pk>\d+)/$',
        UserPlanDetailView.as_view(), name='userplan_detail'),
    url(r'^userplans/(?P<pk>\d+)/start/$',
        StartUserPlanView.as_view(), name='start_userplan'),
    url(r'^userplans/(?P<pk>\d+)/booking/$',
        BookingView.as_view(), name='booking'),
    url(r'^userplans/(?P<plan_pk>\d+)/days/(?P<pk>\d+)/add_weight/$',
        AddWeightView.as_view(), name='add_weight'),
)
