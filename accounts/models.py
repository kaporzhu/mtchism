# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from buildings.models import Building


class Profile(models.Model):
    """
    User profile model
    """
    user = models.OneToOneField(User)
    building = models.ForeignKey(Building, null=True)
    location = models.CharField(max_length=128, blank=True)
    preferred_breakfast_time = models.CharField(max_length=16, blank=True)
    preferred_lunch_time = models.CharField(max_length=16, blank=True)
    preferred_supper_time = models.CharField(max_length=16, blank=True)


def create_user_profile(sender, instance, created, **kwargs):
    """
    Create User profile when new User is added
    """
    if created:
        Profile(user=instance).save()

post_save.connect(create_user_profile, User)
