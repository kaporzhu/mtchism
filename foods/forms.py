# -*- coding: utf-8 -*-
import json

from django import forms


class UploadFoodForm(forms.Form):
    """
    Upload food data form.
    """
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}))

    def clean(self):
        """
        Add the JSON object to the cleaned data if it's valid.
        """
        cleaned_data = super(UploadFoodForm, self).clean()
        json_file = cleaned_data.get('file')
        if json_file:
            try:
                cleaned_data['foods'] = json.loads(json_file.read())
            except ValueError:
                raise forms.ValidationError('Invalid JSON file')

        return cleaned_data
