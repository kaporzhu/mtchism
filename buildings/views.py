# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, SetHeadlineMixin, StaffuserRequiredMixin
)

from .mixins import NewTagMixin
from .models import Building, Tag


class BuildingListView(StaffuserRequiredMixin, ListView):
    """
    Display all the buildings
    """
    model = Building

    def get_context_data(self, **kwargs):
        """
        Add tags to context
        """
        data = super(BuildingListView, self).get_context_data(**kwargs)
        data.update({'tags': Tag.objects.all()})
        data.update(self.request.GET.items())
        return data

    def get_queryset(self):
        """
        Add tag filter to the queryset
        """
        qs = super(BuildingListView, self).get_queryset()
        tag_name = self.request.GET.get('tag', 'all')
        tag_Q = Q(tags__name=tag_name) if tag_name != 'all' else Q()
        return qs.filter(tag_Q)


class CreateBuildingView(SuperuserRequiredMixin, SetHeadlineMixin, NewTagMixin,
                         CreateView):
    """
    Create new building
    """
    headline = u'添加新的写字楼'
    model = Building
    success_url = reverse_lazy('buildings:list')


class UpdateBuildingView(SuperuserRequiredMixin, SetHeadlineMixin, NewTagMixin,
                         UpdateView):
    """
    Update building properties
    """
    headline = u'编辑写字楼信息'
    model = Building
    success_url = reverse_lazy('buildings:list')
