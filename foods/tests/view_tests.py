# -*- coding: utf-8 -*-
import os

from django.contrib.messages.storage.fallback import FallbackStorage
from django.test.client import RequestFactory
from django.test.testcases import TestCase

from foods.forms import UploadFoodForm
from foods.models import Category, Food
from foods.views import UploadFoodView
from mtchism.tests.mixins import FormFileMixin


class UploadFoodViewTests(FormFileMixin, TestCase):
    """
    Tests for UploadFoodView
    """
    def test_form_valid(self):
        """
        Check if the data are added to the database.
        """
        view = UploadFoodView()
        request = RequestFactory()
        request.session = {}
        request._messages = FallbackStorage(request)
        view.request = request
        test_data_folder = os.path.join(os.path.dirname(__file__), 'data')

        # valid foods
        self.assertFalse(Category.objects.exists())
        self.assertFalse(Food.objects.exists())
        test_data_file = os.path.join(test_data_folder, 'valid_foods.json')
        files = self.create_file_data(test_data_file, 'file')
        form = UploadFoodForm(files=files)
        self.assertTrue(form.is_valid())
        view.form_valid(form)
        self.assertTrue(Category.objects.count() == 1)
        self.assertTrue(Food.objects.count() == 1)

        # invalid foods
        test_data_file = os.path.join(test_data_folder, 'invalid_foods.json')
        files = self.create_file_data(test_data_file, 'file')
        form = UploadFoodForm(files=files)
        self.assertTrue(form.is_valid())
        view.form_valid(form)
        self.assertTrue(Category.objects.count() == 1)
        self.assertTrue(Food.objects.count() == 1)
