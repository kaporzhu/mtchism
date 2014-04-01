# -*- coding: utf-8 -*-
import os

from django.test.testcases import TestCase

from foods.forms import UploadFoodForm
from mtchism.tests.mixins import FormFileMixin


class UploadFoodFormTests(FormFileMixin, TestCase):
    """
    Tests for UploadFoodForm
    """

    def test_clean(self):
        """
        Case 1: Upload an empty file
        Case 2: Upload invalid JSON file
        Case 3: Upload valid JSON file
        Case 4: Upload invalid food JSON file
        """
        test_data_folder = os.path.join(os.path.dirname(__file__), 'data')

        # case 1
        test_data_file = os.path.join(test_data_folder, 'empty.json')
        files = self.create_file_data(test_data_file, 'file')
        form = UploadFoodForm(files=files)
        self.assertFalse(form.is_valid())

        # case 2
        test_data_file = os.path.join(test_data_folder, 'invalid_json.json')
        files = self.create_file_data(test_data_file, 'file')
        form = UploadFoodForm(files=files)
        self.assertFalse(form.is_valid())

        # case 3
        test_data_file = os.path.join(test_data_folder, 'valid_foods.json')
        files = self.create_file_data(test_data_file, 'file')
        form = UploadFoodForm(files=files)
        self.assertTrue(form.is_valid())

        # case 4
        test_data_file = os.path.join(test_data_folder, 'invalid_foods.json')
        files = self.create_file_data(test_data_file, 'file')
        form = UploadFoodForm(files=files)
        self.assertTrue(form.is_valid())
