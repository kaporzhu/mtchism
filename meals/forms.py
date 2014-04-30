# -*- coding: utf-8 -*-
import json

from django import forms

from .models import Meal, Dish


class MealForm(forms.ModelForm):
    """
    Model form for CreateMealView and UpdateMealView
    """
    class Meta:
        model = Meal
        fields = ('name', 'price', 'limitations', 'category', 'is_active')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '套餐名'}),
            'price': forms.TextInput(
                attrs={'type': 'number', 'class': 'form-control'}),
            'limitations': forms.CheckboxSelectMultiple(
                choices=Meal.MEAL_TYPE_CHOICES)
        }

    def clean_limitations(self):
        """
        Convert limitations to JSON string
        """
        return json.dumps(self.data.getlist('limitations'))


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


class UpdateDishFoodsForm(forms.Form):
    """
    Form for update dish foods
    """
    foods = forms.CharField(widget=forms.HiddenInput)

    def clean_foods(self):
        """
        Convert the foods string to JSON
        """
        try:
            foods = json.loads(self.data.get('foods'))
            return foods
        except:
            raise forms.ValidationError('Invalid foods data')
