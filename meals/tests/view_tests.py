# -*- coding: utf-8 -*-
from django.test.client import RequestFactory
from django.test.testcases import TestCase

import mock

from .factories import MealFactory, DishFactory
from accounts.tests.factories import UserFactory
from foods.tests.factories import FoodFactory
from meals.forms import MealForm, DishForm, UpdateDishFoodsForm
from meals.models import Meal, Dish, DishFood
from meals.views import(
    CreateMealView, CreateDishView, UpdateDishFoodsView, MealIndexView
)


class CreateMealViewTests(TestCase):
    """
    Tests for CreateMealView
    """
    def _fake_form_valid(self, form):
        """
        Fake form_valid, return None directly
        """
        return None

    @mock.patch('django.views.generic.edit.CreateView.form_valid',
                _fake_form_valid)
    def test_form_valid(self):
        """
        Check if the meal object is created
        """
        # create view
        user = UserFactory()
        request = RequestFactory()
        request.user = user
        view = CreateMealView()
        view.request = request

        # create form
        form = MealForm({'name': 'Meal name'})

        # test now
        view.form_valid(form)
        self.assertTrue(Meal.objects.filter(name='Meal name').exists())


class CreateDishViewTest(TestCase):
    """
    Tests for CreateDishView
    """
    def _fake_post(self, request, *args, **kwargs):
        """
        Fake post, return None directly
        """
        return None

    @mock.patch('django.views.generic.edit.CreateView.post', _fake_post)
    def test_post(self):
        """
        Check if the meal is set to the view
        """
        meal = MealFactory()
        view = CreateDishView()
        view.post(None, meal_pk=meal.id)
        self.assertTrue(view.meal == meal)

    def _fake_form_valid(self, form):
        """
        Fake form_valid, return None directly
        """
        return None

    @mock.patch('django.views.generic.edit.CreateView.form_valid',
                _fake_form_valid)
    def test_form_valid(self):
        """
        Check if the dish is created and added to the meal
        """
        # create view
        meal = MealFactory()
        request = RequestFactory()
        request.user = meal.creator
        view = CreateDishView()
        view.request = request
        view.meal = meal

        # create form
        form = DishForm({'name': 'Dish name'})

        # test now
        view.form_valid(form)
        self.assertTrue(Dish.objects.filter(name='Dish name').exists())
        self.assertTrue(view.meal.dishes.filter(name='Dish name').exists())


class UpdateDishFoodsViewTests(TestCase):
    """
    Tests for UpdateDishFoodsView
    """
    def _fake_dispatch(self, request, *args, **kwargs):
        """
        Fake dispatch, return None directly.
        """
        return None

    @mock.patch('django.views.generic.edit.FormView.dispatch', _fake_dispatch)
    @mock.patch('braces.views.StaffuserRequiredMixin.dispatch', _fake_dispatch)
    def test_dispatch(self):
        """
        Check if the meal and dish are added to the view
        """
        view = UpdateDishFoodsView()
        meal = MealFactory()
        dish = DishFactory()
        view.dispatch(None, meal_pk=meal.id, dish_pk=dish.id)
        self.assertTrue(view.meal == meal)
        self.assertTrue(view.dish == dish)

    def _fake_get_context_data(self, **kwargs):
        """
        Fake get_context_data, return empty dict directly
        """
        return {}

    @mock.patch('django.views.generic.edit.FormView.get_context_data',
                _fake_get_context_data)
    def test_get_context_data(self):
        """
        Check if meal and dish are added to the context
        """
        view = UpdateDishFoodsView()
        view.dish = DishFactory()
        view.meal = MealFactory()
        data = view.get_context_data()
        self.assertTrue('meal' in data)
        self.assertTrue('dish' in data)

    def _fake_form_valid(self, form):
        """
        Fake form_valid, return None directly
        """
        return None

    @mock.patch('django.views.generic.edit.FormView.form_valid',
                _fake_form_valid)
    def test_form_valid(self):
        """
        1. Add new dishfood
        2. Update existed dishfood
        3. Remove dishfood
        """
        food = FoodFactory()
        dish = DishFactory()
        form = UpdateDishFoodsForm()
        request = RequestFactory()
        request.user = dish.creator
        view = UpdateDishFoodsView()
        view.dish = dish
        view.request = request

        # new dishfood added
        DishFood.objects.all().delete()
        form.cleaned_data = {
            'foods': [{'id': food.id, 'weight': 0}]
        }
        view.form_valid(form)
        self.assertTrue(DishFood.objects.exists())

        # dishfood updated
        dishfood = DishFood.objects.first()
        form.cleaned_data = {
            'foods': [{'dishfood_id': dishfood.id, 'id': food.id, 'weight': 1}]
        }
        view.form_valid(form)
        self.assertTrue(DishFood.objects.get(pk=dishfood.id).weight == 1)

        # dishfood removed
        form.cleaned_data = {'foods': []}
        view.form_valid(form)
        self.assertFalse(DishFood.objects.exists())


class MealIndexViewTests(TestCase):
    """
    Tests for MealIndexView
    """
    def _fake_get_context_data(self, **kwargs):
        """
        Fake get_context_data, return empty dict directly
        """
        return {}

    @mock.patch('django.views.generic.base.TemplateView.get_context_data',
                _fake_get_context_data)
    def test_get_context_data(self):
        """
        Check if the meals is added to the context
        """
        view = MealIndexView()
        data = view.get_context_data()
        self.assertTrue('meals' in data)
