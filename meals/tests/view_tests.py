# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.test.testcases import TestCase

import mock

from foods.models import Food, Category
from meals.forms import MealForm, DishForm, UpdateDishFoodsForm
from meals.models import Meal, Dish, DishFood
from meals.views import CreateMealView, CreateDishView, UpdateDishFoodsView


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
        user, created = User.objects.get_or_create(username='12345678901')
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
        user, created = User.objects.get_or_create(username='12345678901')
        meal, created = Meal.objects.get_or_create(name='meal', creator=user)
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
        user, created = User.objects.get_or_create(username='12345678901')
        meal, created = Meal.objects.get_or_create(name='meal', creator=user)
        request = RequestFactory()
        request.user = user
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
        user, created = User.objects.get_or_create(username='test')
        meal, created = Meal.objects.get_or_create(creator=user, name='meal')
        dish, created = Dish.objects.get_or_create(creator=user, name='dish')
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
        user, created = User.objects.get_or_create(username='test')
        meal, created = Meal.objects.get_or_create(creator=user, name='meal')
        dish, created = Dish.objects.get_or_create(creator=user, name='dish')
        view.dish = dish
        view.meal = meal
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
        category, created = Category.objects.get_or_create(name='category')
        food, created = Food.objects.get_or_create(name='food',
                                                   category=category)
        user, created = User.objects.get_or_create(username='test')
        dish, created = Dish.objects.get_or_create(creator=user, name='dish')
        form = UpdateDishFoodsForm()
        request = RequestFactory()
        request.user = user
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
