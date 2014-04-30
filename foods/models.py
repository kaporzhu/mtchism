# -*- coding: utf-8 -*-
from django.db import models


class Category(models.Model):
    """
    Model for food category
    """
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Food(models.Model):
    """
    Model for food material.
    """
    name = models.CharField(max_length=128, db_index=True)
    category = models.ForeignKey(Category)
    origin_id = models.IntegerField(db_index=True, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    # 营养信息(每100克)
    heat = models.FloatField(default=-1)  # 热量（大卡）
    carbohydrate = models.FloatField(default=-1)  # 碳水化合物（克）
    fat = models.FloatField(default=-1)  # 脂肪（克）
    protein = models.FloatField(default=-1)  # 蛋白质（克）
    cellulose = models.FloatField(default=-1)  # 纤维素（克）

    def __unicode__(self):
        return self.name
