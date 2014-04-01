# -*- coding: utf-8 -*-
from django import forms
from django.contrib import auth


class LoginForm(forms.Form):
    """
    Form for user login.
    """
    username = forms.CharField(label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        """
        Check the username and password here
        """
        data = self.data
        username = data['username']
        password = data['password']

        if not auth.authenticate(username=username, password=password):
            raise forms.ValidationError('用户名或者密码错误，请重试')
        return data
