# -*- coding: utf-8 -*-
from django.test.testcases import TestCase

from .factories import UserFactory
from accounts.models import Profile


class SignalTests(TestCase):
    """
    Tests for model signal handler
    """
    def test_create_user_profile(self):
        """
        Check if the profile is created if new User created
        """
        user = UserFactory()
        self.assertTrue(Profile.objects.filter(user=user).exists())


class ProfileTests(TestCase):
    """
    Tests for Profile model
    """
    def test_unicode(self):
        user = UserFactory()
        self.assertEqual(str(user.profile), user.username)
