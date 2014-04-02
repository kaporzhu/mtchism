# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.test.testcases import TestCase

import mock

from meals.forms import MealForm, DishForm
from meals.models import Meal, Dish
from meals.views import CreateMealView, CreateDishView


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
