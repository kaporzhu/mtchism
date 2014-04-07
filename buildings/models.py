# -*- coding: utf-8 -*-
from django.db import models


class Tag(models.Model):
    """
    Tag for building.
    Might be the area, hot, active
    """
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Building(models.Model):
    """
    Office building model
    """
    name = models.CharField(u'名字', max_length=128)
    address = models.CharField(u'详细地址', max_length=128)
    tips = models.TextField(u'备注', blank=True)
    tags = models.ManyToManyField(to=Tag, verbose_name=u'分类')
    is_active = models.BooleanField(u'开放购买', default=True)
