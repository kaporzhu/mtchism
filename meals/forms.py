# -*- coding: utf-8 -*-
from django import forms

from .models import Meal


class MealForm(forms.ModelForm):
    """
    Model form for CreateMealView and UpdateMealView
    """
    class Meta:
        model = Meal
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': '套餐名'})
        }
