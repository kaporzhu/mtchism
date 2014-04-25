# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import StaffuserRequiredMixin

from .forms import PlanForm
from .models import Plan


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
