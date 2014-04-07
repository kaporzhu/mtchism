# -*- coding: utf-8 -*-
from django.http.request import QueryDict
from django.test.testcases import TestCase

from buildings.mixins import NewTagMixin
from buildings.models import Tag


class NewTagMixinTests(TestCase):
    """
    Tests for NewTagMixin
    """

    def test_get_form_kwargs(self):
        """
        Check if the new tag is added
        """
        class View(object):
            def get_form_kwargs(self):
                return {'data': QueryDict('tags=new_tag')}

        class TestView(NewTagMixin, View):
            pass

        TestView().get_form_kwargs()
        self.assertTrue(Tag.objects.filter(name='new_tag').exists())
