# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test.testcases import TestCase

from orders.utils import get_tomorrow


class UtilTests(TestCase):
    """
    Test the util functions
    """

    def test_get_tomorrow(self):
        """
        Check if tomorrow is returned.
        """
        self.assertIn(
            get_tomorrow().date(),
            [datetime.now().date(), datetime.now().date() + timedelta(days=1)])
