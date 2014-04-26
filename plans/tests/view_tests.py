# -*- coding: utf-8 -*-
from django.test.client import RequestFactory
from django.test.testcases import TestCase

import mock

from accounts.tests.factories import UserFactory
from meals.tests.factories import MealFactory
from plans.constants import BREAKFAST
from plans.forms import PlanForm, StageForm, StageMealForm
from plans.models import Plan, Stage, UserPlan, StageMeal
from plans.tests.factories import PlanFactory, UserPlanFactory, StageFactory,\
    StageMealFactory
from plans.views import(
    CreatePlanView, CreateStageView, IndexView, JoinPlanView,
    CreateMealView, UpdateMealView, MealListView
)


class CreatePlanViewTests(TestCase):
    """
    Tests for CreatePlanView
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
        Check if the plan is created
        """
        name = 'test create view'
        form = PlanForm({'name': name, 'is_active': 'on'})
        form.is_valid()
        request = RequestFactory()
        request.user = UserFactory()
        view = CreatePlanView()
        view.request = request
        view.form_valid(form)
        self.assertTrue(Plan.objects.filter(name=name).exists())


class CreateStageViewTests(TestCase):
    """
    Tests for CreateStageView
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
        Check if the plan is created
        """
        plan = PlanFactory()
        name = 'test create view'
        form = StageForm({'name': name, 'days': '10', 'index': '1'})
        form.is_valid()
        request = RequestFactory()
        request.user = UserFactory()
        view = CreateStageView()
        view.request = request
        view.kwargs = {'plan_pk': plan.id}
        view.form_valid(form)
        self.assertTrue(Stage.objects.filter(name=name).exists())


class IndexViewTests(TestCase):
    """
    Tests for IndexView
    """
    def _fake_get_context_data(self):
        """
        Fake get_context_data, return empty dict directly
        """
        return {}

    @mock.patch('django.views.generic.base.TemplateView.get_context_data',
                _fake_get_context_data)
    def test_get_context_data(self):
        """
        Check if user plans and other plans are added to the context.
        """
        plan = PlanFactory()
        other_plan = PlanFactory()
        user = UserFactory()
        user_plan = UserPlanFactory(user=user, plan=plan)
        request = RequestFactory()
        request.user = user
        view = IndexView()
        view.request = request
        data = view.get_context_data()
        self.assertIn(user_plan, data['user_plans'])
        self.assertIn(other_plan, data['other_plans'])

        user.is_authenticated = lambda: False
        data = view.get_context_data()
        self.assertListEqual([plan, other_plan],
                             list(data['other_plans']))


class JoinPlanViewTests(TestCase):
    """
    Tests for JoinPlanView
    """
    def _fake_get_redirect_url(self, *args, **kwargs):
        """
        Fake get_redirect_url, return empty dict directly
        """
        return None

    @mock.patch('django.views.generic.base.RedirectView.get_redirect_url',
                _fake_get_redirect_url)
    def test_get_redirect_url(self):
        """
        Check user plan is created
        """
        plan = PlanFactory()
        request = RequestFactory()
        request.user = UserFactory()
        view = JoinPlanView()
        view.request = request
        view.get_redirect_url(pk=plan.id)
        self.assertTrue(UserPlan.objects.filter(plan=plan).exists())


class CreateMealViewTests(TestCase):
    """
    Tests for CreateMealView
    """
    def test_get_success_url(self):
        """
        Check the success url
        """
        view = CreateMealView()
        view.kwargs = {'plan_pk': 1, 'stage_pk': 2}
        url = view.get_success_url()
        self.assertEqual(url, '/plans/1/stages/2/meals/list/')

    def _fake_form_valid(self, *args, **kwargs):
        """
        Fake form_valid, return empty dict directly
        """
        return None

    @mock.patch('django.views.generic.edit.CreateView.form_valid',
                _fake_form_valid)
    def test_form_valid(self):
        """
        Check if the new stage meal is created
        """
        stage = StageFactory()
        meal = MealFactory()
        request = RequestFactory()
        request.user = UserFactory()
        view = CreateMealView()
        view.request = request
        view.kwargs = {'stage_pk': stage.id}
        form = StageMealForm({'meal': meal.id, 'category': BREAKFAST})
        view.form_valid(form)
        self.assertTrue(
            StageMeal.objects.filter(meal=meal, stage=stage).exists())


class UpdateMealViewTests(TestCase):
    """
    Tests for UpdateMealView
    """
    def test_get_success_url(self):
        """
        Check the success url
        """
        view = UpdateMealView()
        view.kwargs = {'plan_pk': 1, 'stage_pk': 2}
        url = view.get_success_url()
        self.assertEqual(url, '/plans/1/stages/2/meals/list/')


class MealListViewTests(TestCase):
    """
    Tests for MealListView
    """
    def _fake_get_context_data(self):
        """
        Fake get_context_data, return empty dict directly
        """
        return {}

    @mock.patch('django.views.generic.list.ListView.get_context_data',
                _fake_get_context_data)
    def test_get_context_data(self):
        """
        Check if the kwargs is added to the context
        """
        view = MealListView()
        view.kwargs = {'key': 'value'}
        data = view.get_context_data()
        self.assertEqual(data, view.kwargs)

    def test_get_queryset(self):
        """
        Check if only the stage meals are returned
        """
        stage = StageFactory()
        stage_meal_one = StageMealFactory(stage=stage)
        stage_meal_two = StageMealFactory()
        view = MealListView()
        view.kwargs = {'stage_pk': stage.id}
        qs = view.get_queryset()
        self.assertIn(stage_meal_one, qs)
        self.assertNotIn(stage_meal_two, qs)
