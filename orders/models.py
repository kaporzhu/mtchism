# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from .constant import(
    CREATED, PAID, DONE, CANCELED
)
from buildings.models import Building
from meals.constant import LUNCH
from meals.models import Meal


class Order(models.Model):
    """
    Model for order
    """

    STATUS_CHOICES = (
        (CREATED, u'等待付款'),
        (PAID, u'等待配送'),
        (DONE, u'已完成'),
        (CANCELED, u'已取消'),
    )

    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default=CREATED)
    total_price = models.FloatField(default=0)
    total_amount = models.IntegerField(default=0)
    building = models.ForeignKey(Building, null=True)
    location = models.CharField(max_length=256, blank=True)
    deliver_time = models.CharField(max_length=16, blank=True)
    deliver_date = models.DateField(auto_now_add=True)
    meal_type = models.CharField(max_length=16, choices=Meal.MEAL_TYPE_CHOICES,
                                 default=LUNCH)
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def get_operation_buttons(self):
        """
        Depends on the order status.
        If the order isn't paid, the user can cancel or pay.
        """
        if self.status == CREATED:
            cancel_url = reverse('orders:cancel', kwargs={'pk': self.id})
            cancel_btn = '<a href="javascript:void(0)" data-url="{}" '\
                         'data-message="确定要取消？" class="confirm btn '\
                         'btn-default btn-xs pull-right">'\
                         '取消订单</a>'.format(cancel_url)
            pay_url = '#'
            pay_btn = '<a href="{}" class="btn btn-primary btn-xs '\
                      'pull-right">马上支付</a>'.format(pay_url)
            return '{}{}'.format(cancel_btn, pay_btn)

        return None

    @classmethod
    def get_status_label(cls, status):
        """
        Get the status display from status
        """
        for choice in cls.STATUS_CHOICES:
            if choice[0] == status:
                return choice[1]
        raise ValueError('Invalid status value')


class OrderMeal(models.Model):
    """
    Meal for order
    """
    meal = models.ForeignKey(Meal)
    order = models.ForeignKey(Order)
    amount = models.IntegerField()
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
