# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Plan, Stage, StageMeal, UserPlan, UserStage, UserStageDay


admin.site.register(Plan)
admin.site.register(Stage)
admin.site.register(StageMeal)
admin.site.register(UserPlan)
admin.site.register(UserStage)
admin.site.register(UserStageDay)
