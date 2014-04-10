# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView

from braces.views import(
    StaffuserRequiredMixin, SetHeadlineMixin
)

from .forms import MealForm, DishForm, UpdateDishFoodsForm
from .models import Meal, Dish, DishFood, MealCategory
from foods.models import Food


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
    View for update meal
    """
    model = Meal
    form_class = MealForm
    headline = '修改套餐名'
    success_url = reverse_lazy('meals:list')

    def get_form_kwargs(self):
        """
        Convert limitation to a string
        """
        kwargs = super(UpdateMealView, self).get_form_kwargs()
        if kwargs['instance'].limitations:
            limitations = json.loads(kwargs['instance'].limitations)
        else:
            limitations = []
        kwargs['instance'].limitations = limitations
        return kwargs


class MealListView(StaffuserRequiredMixin, ListView):
    """
    List view for meals
    """
    model = Meal

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(MealListView, self).get_context_data(**kwargs)
        data.update({'categories': MealCategory.objects.all(),
                     'meal_type_choices': Meal.MEAL_TYPE_CHOICES})
        data.update(self.request.GET.dict())
        return data

    def get_queryset(self):
        """
        Add more filters to the queryset
        """
        qs = super(MealListView, self).get_queryset()

        # category
        cat_id = self.request.GET.get('category', 'all')
        if cat_id == 'all':
            category_Q = Q()
        else:
            category_Q = Q(categories=MealCategory.objects.get(pk=cat_id))

        # meal type
        meal_type = self.request.GET.get('meal_type', 'all')
        meal_type_Q = Q(limitations__icontains=meal_type) if meal_type != 'all' else Q()  # noqa

        return qs.filter(category_Q, meal_type_Q)


class CreateDishView(StaffuserRequiredMixin, SetHeadlineMixin, CreateView):
    """
    View for create dish
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
        Set the dish creator here.
        And add new dish to the meal
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
    View for update dish
    """
    model = Dish
    form_class = DishForm
    headline = '修改菜名'
    success_url = reverse_lazy('meals:list')


class UpdateDishFoodsView(StaffuserRequiredMixin, FormView):
    """
    View for updates foods in dish
    """
    form_class = UpdateDishFoodsForm
    success_url = reverse_lazy('meals:list')
    template_name = 'meals/update_dish_foods.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Get meal from meal_pk, dish from dish_pk
        """
        self.meal = Meal.objects.get(pk=kwargs['meal_pk'])
        self.dish = Dish.objects.get(pk=kwargs['dish_pk'])
        return super(UpdateDishFoodsView, self).dispatch(request, *args, **kwargs)  # noqa

    def get_context_data(self, **kwargs):
        """
        Add extra data to the context
        """
        data = super(UpdateDishFoodsView, self).get_context_data(**kwargs)
        data.update({'meal': self.meal, 'dish': self.dish})
        return data

    def form_valid(self, form):
        """
        Update dish foods here
        """
        foods_json = form.cleaned_data['foods']
        old_food_ids = [f.id for f in self.dish.dishfood_set.all()]
        new_food_ids = []
        for food_json in foods_json:
            if food_json.get('dishfood_id') in old_food_ids:
                dishfood = DishFood.objects.get(pk=food_json['dishfood_id'])
                dishfood.weight = float(food_json['weight'])
            else:
                dishfood = DishFood()
                dishfood.food = Food.objects.get(pk=food_json['id'])
                dishfood.creator = self.request.user
                dishfood.dish = self.dish
                dishfood.weight = float(food_json['weight'])
            dishfood.save()
            new_food_ids.append(dishfood.id)

        self.dish.dishfood_set.exclude(id__in=new_food_ids).delete()

        return super(UpdateDishFoodsView, self).form_valid(form)


class MealIndexView(TemplateView):
    """
    View for display all the meals
    """
    template_name = 'meals/index.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(MealIndexView, self).get_context_data(**kwargs)
        # get meals by category
        category_id = int(self.request.GET.get('cat', '1'))
        category = MealCategory.objects.get(pk=category_id)
        data.update({'meals': Meal.objects.filter(is_active=True, categories=category),  # noqa
                     'category_id': category_id,
                     'meal_types': Meal.MEAL_TYPES,
                     'meal_categories': MealCategory.objects.all()})
        return data
