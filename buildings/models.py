# -*- coding: utf-8 -*-
from django.db import models


class Tag(models.Model):
    """
    Tag for building.
    Might be the area, hot, active
    """
    name = models.CharField(max_length=64)


class Building(models.Model):
    """
    Office building model
    """
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    tips = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    is_active = models.BooleanField(default=True)
