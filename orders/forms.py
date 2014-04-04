# -*- coding: utf-8 -*-
import json

from django import forms


class CheckoutForm(forms.Form):
    """
    Form for checkout meals
    """
    address = forms.CharField(widget=forms.HiddenInput)
    meals = forms.CharField(widget=forms.HiddenInput)

    def clean_meals(self):
        """
        Check meals if it's a valid JSON string
        """
        try:
            return json.loads(self.data.get('meals'))
        except ValueError:
            raise forms.ValidationError('套餐信息数据的格式不对')
