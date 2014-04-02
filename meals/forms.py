# -*- coding: utf-8 -*-
from django import forms

from .models import Meal, Dish


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


class DishForm(forms.ModelForm):
    """
    Model form for CreateDishView and UpdateDishView
    """
    class Meta:
        model = Dish
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': '菜名'})
        }
