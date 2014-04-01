# -*- coding: utf-8 -*-
from django import forms
from django.test.testcases import TestCase

from accounts.mixins import PhoneFormMixin


class PhoneFormMixinTests(TestCase):
    """
    Tests for PhoneFormMixin
    """
    def test_clean_username(self):
        """
        Check username as phone number
        """
        mixin = PhoneFormMixin()

        # invalid number
        mixin.data = {'username': '123'}
        self.assertRaises(forms.ValidationError,
                          lambda: mixin.clean_username())

        # valid number
        mixin.data = {'username': '12345678900'}
        self.assertTrue(mixin.clean_username() == '12345678900')
