# -*- coding: utf-8 -*-
from django import template, forms
from django.test.testcases import TestCase


class MtCHIsmTemplateTagTests(TestCase):
    """
    Tests for mtchism template tags
    """
    def test_add_attr(self):
        """
        Check if the new attr is added to the field
        """
        class Form(forms.Form):
            name = forms.CharField()

        tpl = template.Template(
            '{% load mtchism_template_tags %}'
            '{{ form.name|add_attr:"class,hidden" }}')
        rendered = tpl.render(template.Context({'form': Form()}))
        self.assertTrue('class="hidden"' in rendered)

    def test_is_checkbox(self):
        """
        Check if the field is a checkbox
        """
        class Form(forms.Form):
            active = forms.BooleanField()

        tpl = template.Template(
            '{% load mtchism_template_tags %}'
            '{{ form.active|is_checkbox }}')
        rendered = tpl.render(template.Context({'form': Form()}))
        self.assertTrue(rendered == 'True')
