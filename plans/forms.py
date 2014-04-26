# -*- coding: utf-8 -*-
from django import forms

from .models import Plan, Stage, StageMeal


class PlanForm(forms.ModelForm):
    """
    Plan model form. Used by Create and Update views.
    """
    class Meta:
        model = Plan
        fields = ('name', 'is_active',)


class StageForm(forms.ModelForm):
    """
    Stage model form.
    """
    class Meta:
        model = Stage
        fields = ('name', 'days', 'index',)


class StageMealForm(forms.ModelForm):
    """
    Stage meal model form
    """
    class Meta:
        model = StageMeal
        fields = ('category', 'meal',)
