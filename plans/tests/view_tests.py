# -*- coding: utf-8 -*-
from django.test.client import RequestFactory
from django.test.testcases import TestCase

import mock

from accounts.tests.factories import UserFactory
from plans.forms import PlanForm, StageForm
from plans.models import Plan, Stage
from plans.tests.factories import PlanFactory
from plans.views import CreatePlanView, CreateStageView


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
