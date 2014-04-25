# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test.testcases import TestCase

from .factories import PlanFactory, StageFactory, UserPlanFactory
from plans.constants import JOINED, RUNNING, GIVENUP, DONE
from plans.models import UserStage


class PlanTests(TestCase):
    """
    Tests for model Plan
    """
    def test_days_property(self):
        """
        Check if the sum of stage days is returned
        """
        plan = PlanFactory()
        stage_one = StageFactory(plan=plan, days=1)
        stage_two = StageFactory(plan=plan, days=2)
        self.assertEqual(plan.days, stage_one.days + stage_two.days)


class UserPlanTests(TestCase):
    """
    Tests for UserPlan model
    """
    def test_start(self):
        """
        Check:
            1. status is updated
            2. started and ended date is updated
            3. user stages are created
            4. current stage is set to the new created user stage
            5. chrrent stage is set to running
        """
        plan = PlanFactory()
        stage_one = StageFactory(plan=plan, days=1, index=1)
        stage_two = StageFactory(plan=plan, days=2, index=2)
        user_plan = UserPlanFactory(plan=plan, status=JOINED)
        user_plan.start()

        self.assertEqual(user_plan.status, RUNNING)
        self.assertIsNotNone(user_plan.started_at)
        self.assertIsNotNone(user_plan.ended_at)
        self.assertEqual(user_plan.current_stage.status, RUNNING)
        user_stages = user_plan.userstage_set.all()
        self.assertEqual(user_stages.count(), 2)
        self.assertTrue(user_stages.filter(stage=stage_one).exists())
        self.assertTrue(user_stages.filter(stage=stage_two).exists())

    def test_give_up(self):
        """
        Check:
            1. status is updated
            2. given_up_at is updated
            3. all the user stages status are updated
        """
        plan = PlanFactory()
        StageFactory(plan=plan, days=1, index=1)
        StageFactory(plan=plan, days=2, index=2)
        user_plan = UserPlanFactory(plan=plan, status=JOINED)
        user_plan.start()
        user_plan.give_up()

        self.assertEqual(user_plan.status, GIVENUP)
        self.assertIsNotNone(user_plan.given_up_at)
        self.assertEqual(
            user_plan.userstage_set.filter(status=GIVENUP).count(), 2)

    def test_validate(self):
        """
        Check if the user plan is ended.
        Check if the stage is ended and auto switch to next stage.
        """
        now = datetime.now()
        plan = PlanFactory()
        stage_one = StageFactory(plan=plan, days=1, index=1)
        stage_two = StageFactory(plan=plan, days=2, index=2)

        # user plan is ended
        user_plan = UserPlanFactory(plan=plan, status=JOINED)
        user_plan.start()
        user_plan.ended_at = now - timedelta(days=1)
        user_plan.save()
        user_plan.validate()
        self.assertEqual(user_plan.status, DONE)

        # stage 1 is ended
        user_plan = UserPlanFactory(plan=plan, status=JOINED)
        user_plan.start()
        user_plan.current_stage.ended_at = now - timedelta(days=1)
        user_plan.current_stage.save()
        user_plan.validate()
        self.assertEqual(user_plan.current_stage.stage, stage_two)
        self.assertEqual(user_plan.current_stage.status, RUNNING)
        self.assertTrue(
            UserStage.objects.filter(status=DONE, stage=stage_one).exists())
