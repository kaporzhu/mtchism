# -*- coding: utf-8 -*-
from django import forms

from .models import Plan


class PlanForm(forms.ModelForm):
    """
    Plan model form. Used by Create and Update views.
    """
    class Meta:
        model = Plan
        fields = ('name', 'is_active',)
