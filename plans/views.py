# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import(
    StaffuserRequiredMixin, LoginRequiredMixin, AjaxResponseMixin,
    JSONResponseMixin
)

from .constants import(
    JOINED, FINISHED, FAILED, UPCOMING, WAITING,
    BREAKFAST, OTHER, SUPPER, LUNCH,
)
from .forms import PlanForm, StageForm, StageMealForm
from .models import Plan, Stage, UserPlan, StageMeal
from plans.models import UserStageDay


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
        data.update({'JOINED': JOINED})
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
        kwargs = {'plan_pk': self.kwargs['plan_pk'],
                  'stage_pk': self.kwargs['stage_pk'],}
        return reverse('plans:meal_list', kwargs=kwargs)


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


class UserPlanDetailView(LoginRequiredMixin, DetailView):
    """
    Detail page for user plan
    """
    model = UserPlan

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(UserPlanDetailView, self).get_context_data(**kwargs)
        user_stages = self.object.userstage_set.all().order_by('index')
        data.update({'user_stages': user_stages})

        # add stage day statuses
        data.update({'FINISHED': FINISHED,
                     'FAILED': FAILED,
                     'UPCOMING': UPCOMING,
                     'WAITING': WAITING})

        return data


class StartUserPlanView(LoginRequiredMixin, RedirectView):
    """
    Start a user plan
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Start the user plan and go to the user plan detail page
        """
        user_plan = UserPlan.objects.get(pk=kwargs['pk'])
        user_plan.start()
        return reverse('plans:userplan_detail', kwargs=kwargs)


class BookingView(LoginRequiredMixin, TemplateView):
    """
    Display all stage meals
    """
    template_name = 'plans/booking.html'

    def get_context_data(self, **kwargs):
        """
        Get all the stage meals and order by category
        """
        data = super(BookingView, self).get_context_data(**kwargs)
        data.update(self.kwargs)
        user_plan = UserPlan.objects.get(pk=self.kwargs['pk'])
        breakfasts = user_plan.current_stage.stage.stagemeal_set.filter(category=BREAKFAST)
        lunches = user_plan.current_stage.stage.stagemeal_set.filter(category=LUNCH)
        suppers = user_plan.current_stage.stage.stagemeal_set.filter(category=SUPPER)
        others = user_plan.current_stage.stage.stagemeal_set.filter(category=OTHER)
        meals = [
            {
                'label': u'早饭',
                'type': BREAKFAST,
                'meals': breakfasts,
                'name': 'breakfast',
                'input_type': 'radio'
            },
            {
                'label': u'午饭',
                'type': LUNCH,
                'meals': lunches,
                'name': 'lunch',
                'input_type': 'radio'
            },
            {
                'label': u'晚饭',
                'type': SUPPER,
                'meals': suppers,
                'name': 'supper',
                'input_type': 'radio'
            },
            {
                'label': u'其他',
                'type': OTHER,
                'meals': others,
                'name': 'other',
                'input_type': 'checkbox'
            }
        ]
        data.update({'meals': meals})
        return data


class AddWeightView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
                    View):
    """
    Set weight for the stage day
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Set weight here
        """
        stage_day = UserStageDay.objects.get(pk=kwargs['pk'])
        stage_day.weight = request.GET['weight']
        stage_day.save()
        return self.render_json_response({'success': True})
