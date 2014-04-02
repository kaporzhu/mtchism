# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from braces.views import(
    StaffuserRequiredMixin, SetHeadlineMixin
)

from .forms import MealForm, DishForm
from .models import Meal, Dish
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


class CreateDishView(StaffuserRequiredMixin, SetHeadlineMixin, CreateView):
    """
    View for create meal
    """
    model = Dish
    form_class = DishForm
    headline = '新建菜品'
    success_url = reverse_lazy('meals:list')

    def post(self, request, *args, **kwargs):
        """
        Get meal from meal_pk
        """
        self.meal = Meal.objects.get(pk=kwargs['meal_pk'])
        return super(CreateDishView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Set the meal creator here
        """
        # create dish
        dish = form.save(commit=False)
        dish.creator = self.request.user
        dish.save()

        # add to meal
        self.meal.dishes.add(dish)

        return super(CreateDishView, self).form_valid(form)


class UpdateDishView(StaffuserRequiredMixin, SetHeadlineMixin, UpdateView):
    """
    View for create meal
    """
    model = Dish
    form_class = DishForm
    headline = '修改菜名'
    success_url = reverse_lazy('meals:list')
