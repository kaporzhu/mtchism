# -*- coding: utf-8 -*-
import re

from django import forms


class PhoneFormMixin(object):
    """
    Mixin for check phone number in the phone
    """
    def clean_username(self):
        """
        Username as the phone number.
        Check it here
        """
        username = self.data.get('username')
        if not re.match('\d{11,11}', username):
            raise forms.ValidationError('手机号不对')
        return username
