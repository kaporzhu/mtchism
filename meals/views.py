# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from braces.views import(
    StaffuserRequiredMixin, SetHeadlineMixin
)

from .forms import MealForm
from .models import Meal
from django.views.generic.list import ListView


class CreateMealView(StaffuserRequiredMixin, SetHeadlineMixin, CreateView):
    """
    View for create meal
    """
    model = Meal
    form_class = MealForm
    headline = '新建套餐'
    success_url = reverse_lazy('meals:list')

    def form_valid(self, form):
        """
        Set the meal creator here
        """
        meal = form.save(commit=False)
        meal.creator = self.request.user
        meal.save()
        return super(CreateMealView, self).form_valid(form)


class UpdateMealView(StaffuserRequiredMixin, SetHeadlineMixin, UpdateView):
    """
    View for create meal
    """
    model = Meal
    form_class = MealForm
    headline = '修改套餐名'
    success_url = reverse_lazy('meals:list')


class MealListView(StaffuserRequiredMixin, ListView):
    """
    List view for meals
    """
    model = Meal
