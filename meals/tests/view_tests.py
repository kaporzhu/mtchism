# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.test.testcases import TestCase

from meals.forms import MealForm
from meals.models import Meal
from meals.views import CreateMealView


class CreateMealViewTests(TestCase):
    """
    Tests for CreateMealView
    """
    def test_form_valid(self):
        """
        Check if the meal object is created
        """
        # create view
        user = User(username='12345678901')
        user.save()
        request = RequestFactory()
        request.user = user
        view = CreateMealView()
        view.request = request

        # create form
        form = MealForm({'name': 'Meal name'})

        # test now
        view.form_valid(form)
        self.assertTrue(Meal.objects.filter(name='Meal name').exists())
