# -*- coding: utf-8 -*-
from django.test.testcases import TestCase

from .factories import TagFactory


class TagTests(TestCase):
    """
    Tests for model Tag
    """
    def test_unicode(self):
        """
        Check if Tag name is returned
        """
        tag = TagFactory.build(name='tag')
        self.assertTrue(tag.name == str(tag))
