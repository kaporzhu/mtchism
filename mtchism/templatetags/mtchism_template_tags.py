# -*- coding: utf-8 -*-
from django import template
from django.forms.widgets import CheckboxInput


register = template.Library()


@register.filter
def add_attrs(field, attrs_str):
    """
    Add attribute to the html tag
    """
    attrs = {}
    for attr in attrs_str.split(';'):
        attr_name, attr_value = attr.split(':')
        attrs[attr_name] = attr_value
    return field.as_widget(attrs=attrs)


@register.filter
def is_checkbox(field):
    """
    Check if the field is a checkbox
    """
    return isinstance(field.field.widget, CheckboxInput)
