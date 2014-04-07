# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, SetHeadlineMixin, StaffuserRequiredMixin
)

from .models import Building


class BuildingListView(StaffuserRequiredMixin, ListView):
    """
    Display all the buildings
    """
    model = Building


class CreateBuildingView(SuperuserRequiredMixin, SetHeadlineMixin, CreateView):
    """
    Create new building
    """
    headline = u'添加新的写字楼'
    model = Building
    success_url = reverse_lazy('buildings:list')


class UpdateBuildingView(SuperuserRequiredMixin, SetHeadlineMixin, UpdateView):
    """
    Update building properties
    """
    headline = u'编辑写字楼信息'
    model = Building
    success_url = reverse_lazy('buildings:list')
