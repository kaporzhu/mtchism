# -*- coding: utf-8 -*-
from django.db import models


class Category(models.Model):
    """
    Model for food category
    """
    name = models.CharField(max_length=128)


class Food(models.Model):
    """
    Model for food material.
    """
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category)

    # 营养信息(每100克)
    heat = models.FloatField()  # 热量（大卡）
    carbohydrate = models.FloatField()  # 碳水化合物（克）
    fat = models.FloatField()  # 脂肪（克）
    protein = models.FloatField()  # 蛋白质（克）
    cellulose = models.FloatField()  # 纤维素（克）
