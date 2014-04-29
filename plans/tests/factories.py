# -*- coding: utf-8 -*-
from datetime import datetime

import factory

from accounts.tests.factories import UserFactory
from meals.tests.factories import MealFactory
from plans.constants import BREAKFAST
from plans.models import(
    Plan, Stage, StageMeal, UserPlan, UserStage, UserStageDay
)


class PlanFactory(factory.DjangoModelFactory):
    """
    Factory for Plan
    """
    FACTORY_FOR = Plan

    name = 'Test plan'
    creator = factory.SubFactory(UserFactory)


class StageFactory(factory.DjangoModelFactory):
    """
    Factory for Stage
    """
    FACTORY_FOR = Stage

    name = 'Stage 1'
    days = 10
    plan = factory.SubFactory(PlanFactory)
    creator = factory.SubFactory(UserFactory)


class StageMealFactory(factory.DjangoModelFactory):
    """
    Factory for StageMeal
    """
    FACTORY_FOR = StageMeal

    stage = factory.SubFactory(StageFactory)
    meal = factory.SubFactory(MealFactory)
    category = BREAKFAST
    creator = factory.SubFactory(UserFactory)


class UserPlanFactory(factory.DjangoModelFactory):
    """
    Factory for UserPlan
    """
    FACTORY_FOR = UserPlan

    user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(PlanFactory)
    days = 10


class UserStageFactory(factory.DjangoModelFactory):
    """
    Factory for UserStage
    """
    FACTORY_FOR = UserStage

    user = factory.SubFactory(UserFactory)
    user_plan = factory.SubFactory(UserPlanFactory)
    stage = factory.SubFactory(StageFactory)
    index = 0


class UserStageDayFactory(factory.DjangoModelFactory):
    """
    Factory for UserStageDay
    """
    FACTORY_FOR = UserStageDay

    user = factory.SubFactory(UserFactory)
    user_stage = factory.SubFactory(UserStageFactory)
    date = datetime.now().date()
