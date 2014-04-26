# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import StaffuserRequiredMixin, LoginRequiredMixin

from .forms import PlanForm, StageForm, StageMealForm
from .models import Plan, Stage, UserPlan, StageMeal


class CreatePlanView(StaffuserRequiredMixin, CreateView):
    """
    Create new plan
    """
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy('plans:list')

    def form_valid(self, form):
        """
        Set creator here.
        """
        plan = form.save(commit=False)
        plan.creator = self.request.user
        plan.save()
        return super(CreatePlanView, self).form_valid(form)


class UpdatePlanView(StaffuserRequiredMixin, UpdateView):
    """
    Update plan
    """
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy('plans:list')


class PlanListView(StaffuserRequiredMixin, ListView):
    """
    Display all the plans for the staff
    """
    model = Plan


class CreateStageView(StaffuserRequiredMixin, CreateView):
    """
    Create stage for plan
    """
    model = Stage
    form_class = StageForm
    success_url = reverse_lazy('plans:list')

    def form_valid(self, form):
        """
        Set extra fields
        """
        stage = form.save(commit=False)
        stage.creator = self.request.user
        stage.plan = Plan.objects.get(pk=self.kwargs['plan_pk'])
        stage.save()
        return super(CreateStageView, self).form_valid(form)


class UpdateStageView(StaffuserRequiredMixin, UpdateView):
    """
    Update stage
    """
    model = Stage
    form_class = StageForm
    success_url = reverse_lazy('plans:list')


class IndexView(TemplateView):
    """
    Plans page
    """
    template_name = 'plans/index.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            user_plans = user.userplan_set.all()
            joined_plan_ids = user_plans.values_list('plan__id', flat=True)
            other_plans = Plan.objects.filter(
                is_active=True).exclude(id__in=joined_plan_ids)
            data.update({'user_plans': user_plans, 'other_plans': other_plans})
        else:
            data.update({'other_plans': Plan.objects.filter(is_active=True)})
        return data


class JoinPlanView(LoginRequiredMixin, RedirectView):
    """
    Join a plan
    """
    permanent = False
    url = reverse_lazy('plans:index')

    def get_redirect_url(self, *args, **kwargs):
        """
        Create UserPlan here
        """
        plan = Plan.objects.get(pk=kwargs['pk'])
        UserPlan(plan=plan, user=self.request.user, days=plan.days).save()
        return super(JoinPlanView, self).get_redirect_url(*args, **kwargs)


class CreateMealView(StaffuserRequiredMixin, CreateView):
    """
    Add meal to the plan stage
    """
    model = StageMeal
    form_class = StageMealForm

    def get_success_url(self):
        return reverse('plans:meal_list', kwargs=self.kwargs)

    def form_valid(self, form):
        """
        Set extra fields for new stage meal
        """
        stage_meal = form.save(commit=False)
        stage_meal.stage = Stage.objects.get(pk=self.kwargs['stage_pk'])
        stage_meal.creator = self.request.user
        stage_meal.save()
        return super(CreateMealView, self).form_valid(form)


class UpdateMealView(StaffuserRequiredMixin, UpdateView):
    """
    Update stage meal
    """
    model = StageMeal
    form_class = StageMealForm

    def get_success_url(self):
        return reverse('plans:meal_list', kwargs=self.kwargs)


class MealListView(StaffuserRequiredMixin, ListView):
    """
    Display stage meals
    """
    model = StageMeal

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(MealListView, self).get_context_data(**kwargs)
        data.update(self.kwargs)
        return data

    def get_queryset(self):
        """
        Get all stage meals for currrent stage
        """
        stage = Stage.objects.get(pk=self.kwargs['stage_pk'])
        return stage.stagemeal_set.all().order_by('category')
