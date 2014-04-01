# -*- coding: utf-8 -*-
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

from .mixins import PhoneFormMixin


class LoginForm(PhoneFormMixin, forms.Form):
    """
    Form for user login.
    """
    username = forms.CharField(
        label='手机号',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='密码',
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


class RegisterForm(PhoneFormMixin, forms.Form):
    """
    Create new account form
    """
    username = forms.CharField(
        label='手机号',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        """
        Check if the user already exist
        """
        username = self.data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('手机号已经存在，是不是忘记了密码？')
        return self.data
