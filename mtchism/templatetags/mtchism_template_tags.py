# -*- coding: utf-8 -*-
from django import template
from django.forms.widgets import CheckboxInput


register = template.Library()


@register.filter
def add_attr(field, attr):
    """
    Add attribute to the html tag
    """
    name, value = attr.split(',')
    return field.as_widget(attrs={name: value})


@register.filter
def is_checkbox(field):
    """
    Check if the field is a checkbox
    """
    return isinstance(field.field.widget, CheckboxInput)
