# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

from .constants import(
    BREAKFAST, LUNCH, SUPPER, OTHER, JOINED, RUNNING, DONE, GIVENUP, READY
)
from meals.models import Meal


class Plan(models.Model):
    """
    Plan model.
    Plan
        Stage
            Meal
    """
    name = models.CharField(u'名字', max_length=64)
    is_active = models.BooleanField(u'启用', default=True)

    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def days(self):
        """
        Get the total days of the whole plan
        """
        days = 0
        for stage in self.stage_set.all():
            days += stage.days
        return days


class Stage(models.Model):
    """
    Plan stage model.
    """
    name = models.CharField(u'名字', max_length=64)
    days = models.SmallIntegerField(u'天数')
    plan = models.ForeignKey(Plan)
    index = models.SmallIntegerField(u'顺序', default=0)

    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)


class StageMeal(models.Model):
    """
    Meal model.
    """

    CATEGORY_CHOICES = (
        (BREAKFAST, u'早餐'),
        (LUNCH, u'午餐'),
        (SUPPER, u'晚餐'),
        (OTHER, u'其他'),
    )

    stage = models.ForeignKey(Stage)
    meal = models.ForeignKey(Meal)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)

    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)


class UserPlan(models.Model):
    """
    User joined plan.
    """

    STATUS_CHOICES = (
        (JOINED, u'已加入'),
        (RUNNING, u'进行中'),
        (DONE, u'已结束'),
        (GIVENUP, u'放弃'),
    )

    user = models.ForeignKey(User)
    plan = models.ForeignKey(Plan)
    days = models.SmallIntegerField()
    current_stage = models.ForeignKey('UserStage', blank=True, null=True)
    current_days = models.SmallIntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES, default=JOINED,
                              max_length=32)
    start_weight = models.FloatField(blank=True, null=True)
    end_weight = models.FloatField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    given_up_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def start(self):
        """
        Start the plan
        """
        if self.status == JOINED:
            self.status = RUNNING
            self.started_at = datetime.now()
            self.ended_at = self.started_at + timedelta(days=self.days)
            self.save()

            # create user stages
            started_at = self.started_at
            for stage in self.plan.stage_set.all():
                ended_at = started_at + timedelta(days=stage.days)
                user_stage = UserStage(user=self.user,
                                       user_plan=self,
                                       stage=stage,
                                       index=stage.index,
                                       started_at=started_at,
                                       ended_at=ended_at)
                user_stage.save()
                started_at = ended_at

            # set current stage
            self.current_stage = self.userstage_set.filter(
                status=READY).order_by('index').first()
            self.current_stage.status = RUNNING
            self.current_stage.save()
            self.save()

    def give_up(self):
        """
        Give up the plan
        """
        if self.status == RUNNING:
            self.status = GIVENUP
            self.given_up_at = datetime.now()
            self.save()
            self.userstage_set.update(status=GIVENUP)

    def validate(self):
        """
        Validate the plan status.
        It should be checked every day in the cron job.
        If reach the end date, update the status.
        """
        if self.status == RUNNING:
            now = datetime.now().date()
            # update user plan status
            if now > self.ended_at.date():
                self.status = DONE
                self.save()

            # update user stage status
            for user_stage in self.userstage_set.all():
                if user_stage.status == RUNNING and now > user_stage.ended_at.date():  # noqa
                    user_stage.status = DONE
                    user_stage.save()

                    # switch user plan to next stage
                    index = user_stage.index
                    next_stage = self.userstage_set.filter(
                        status=READY, index__gt=index).order_by('index').first()  # noqa
                    next_stage.status = RUNNING
                    next_stage.save()
                    self.current_stage = next_stage


class UserStage(models.Model):
    """
    User plan stage.
    """

    STATUS_CHOICES = (
        (READY, u'等待开始'),
        (RUNNING, u'进行中'),
        (DONE, u'已结束'),
        (GIVENUP, u'放弃'),
    )

    user = models.ForeignKey(User)
    user_plan = models.ForeignKey(UserPlan)
    stage = models.ForeignKey(Stage)
    status = models.CharField(choices=STATUS_CHOICES, default=READY,
                              max_length=32)
    index = models.SmallIntegerField()
    start_weight = models.FloatField(blank=True, null=True)
    end_weight = models.FloatField(blank=True, null=True)
    current_days = models.SmallIntegerField(default=0)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)


class UserStageDay(models.Model):
    """
    Day for user stage
    """
    user = models.ForeignKey(User)
    user_stage = models.ForeignKey(UserStage)
    meals = models.ManyToManyField(StageMeal)
    created_at = models.DateTimeField(auto_now_add=True)
