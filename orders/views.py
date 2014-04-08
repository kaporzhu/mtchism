# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from braces.views import(
    LoginRequiredMixin, JSONResponseMixin, StaffuserRequiredMixin,
    AjaxResponseMixin
)

from .constant import CANCELED, DELIVER_TIMES
from .forms import CheckoutForm
from .models import Order, OrderMeal
from buildings.models import Building
from meals.models import Meal


class CheckoutView(LoginRequiredMixin, JSONResponseMixin, FormView):
    """
    View for checkout the meals
    """
    template_name = 'orders/checkout.html'
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        """
        Add buildings to context
        """
        data = super(CheckoutView, self).get_context_data(**kwargs)
        data.update({'buildings': Building.objects.filter(is_active=True),
                     'deliver_times': json.dumps(DELIVER_TIMES),
                     'meal_type_choices': Order.MEAL_TYPE_CHOICES})
        return data

    def form_valid(self, form):
        """
        Create order here
        """
        data = form.cleaned_data
        location = data['location']
        meal_type = data['meal_type']
        deliver_time = data['deliver_time']
        # if it's still earlier than 3am, we think it's yesterday
        now = datetime.now()
        if now.hour >= 0 and now.hour < 3:
            tomorrow = now
        else:
            tomorrow = datetime.now() + timedelta(days=1)
        building = Building.objects.get(pk=data['building'])

        # update user address
        profile = self.request.user.profile
        profile.building = building
        profile.location = location
        profile.save()

        # create order
        order = Order(creator=self.request.user, location=location,
                      building=building, meal_type=meal_type,
                      deliver_time=deliver_time, deliver_date=tomorrow)
        order.save()
        total_price = 0
        total_amount = 0
        for meal_info in data['meals']:
            amount = meal_info['amount']
            meal = Meal.objects.get(pk=meal_info['id'])
            # total_price += meal.price * amount
            total_price += 1.5 * amount
            total_amount += amount
            order_meal = OrderMeal(meal=meal,
                                   creator=self.request.user,
                                   order=order,
                                   amount=meal_info['amount'])
            order_meal.save()
        order.total_price = total_price
        order.total_amount = total_amount
        order.save()

        # return ajax response here
        success_url = reverse('orders:success', kwargs={'pk': order.id})
        context = {'success': True, 'success_url': success_url}
        return self.render_json_response(context)


class MyOrderView(LoginRequiredMixin, TemplateView):
    """
    View for display all my orders
    """
    template_name = 'orders/mine.html'

    def get_context_data(self, **kwargs):
        """
        Add my orders to the context
        """
        data = super(MyOrderView, self).get_context_data(**kwargs)
        orders = Order.objects.filter(creator=self.request.user)
        data.update({'orders': orders})
        return data


class CreateSuccessView(LoginRequiredMixin, DetailView):
    """
    Order create success page
    """
    model = Order
    template_name = 'orders/success.html'


class CancelOrderView(LoginRequiredMixin, RedirectView):
    """
    View for cancel Order
    """
    permanent = False

    def get(self, request, *args, **kwargs):
        """
        Cancel order here
        """
        order = Order.objects.get(pk=kwargs['pk'], creator=self.request.user)
        order.status = CANCELED
        order.save()
        return redirect(reverse('orders:mine'))


class OrderListView(StaffuserRequiredMixin, ListView):
    """
    Display all the orders for the staff
    """
    model = Order

    def get_params_from_request(self):
        """
        Check all params and return as dict
        """
        # status
        status = self.request.GET.get('status')
        status = status if status else 'all'

        # building
        building = self.request.GET.get('building', 'all')

        # location
        location = self.request.GET.get('location', '')

        # meal type
        meal_type = self.request.GET.get('meal-type', 'all')

        # deliver time
        deliver_time = self.request.GET.get('deliver-time', 'all')

        # created time
        try:
            created_start = self.request.GET.get('created-start-datetime')
            created_start_dt = datetime.strptime(created_start,
                                                 '%m/%d/%Y %H:%M')
        except:
            created_start_dt = None
        try:
            created_end = self.request.GET.get('created-end-datetime')
            created_end_dt = datetime.strptime(created_end, '%m/%d/%Y %H:%M')
        except:
            created_end_dt = None

        return {'status': status, 'building': building, 'location': location,
                'meal_type': meal_type, 'deliver_time': deliver_time,
                'created_start_dt': created_start_dt,
                'created_end_dt': created_end_dt}

    def get_queryset(self):
        """
        Display the orders depends on the filters
        """
        qs = super(OrderListView, self).get_queryset()
        params = self.get_params_from_request()

        # status
        status = params['status']
        status_Q = Q(status=status) if status != 'all' else Q()

        # building
        building = params['building']
        if building != 'all':
            building_Q = Q(building=Building.objects.get(pk=building))
        else:
            building_Q = Q()

        # meal type
        meal_type = params['meal_type']
        meal_type_Q = Q(meal_type=meal_type) if meal_type != 'all' else Q()

        # deliver time
        deliver_time = params['deliver_time']
        deliver_time_Q = Q(deliver_time=deliver_time) if deliver_time != 'all' else Q()  # noqa

        # location
        location = params['location']
        location_Q = Q(location__icontains=location) if location else Q()

        # created time
        start_dt = params['created_start_dt']
        end_dt = params['created_end_dt']
        created_time_Q = Q()
        if start_dt and end_dt:
            created_time_Q = Q(created_at__range=(start_dt, end_dt))
        elif start_dt:
            created_time_Q = Q(created_at__gte=start_dt)
        elif end_dt:
            created_time_Q = Q(created_at__lte=end_dt)

        return qs.filter(status_Q, building_Q, meal_type_Q, deliver_time_Q,
                         location_Q, created_time_Q)

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(OrderListView, self).get_context_data(**kwargs)
        data.update({'status_choices': Order.STATUS_CHOICES,
                     'buildings': Building.objects.filter(is_active=True),
                     'meal_type_choices': Order.MEAL_TYPE_CHOICES,
                     'deliver_times': json.dumps(DELIVER_TIMES)})
        data.update(self.get_params_from_request())
        return data


class UpdateOrderStatusView(StaffuserRequiredMixin, JSONResponseMixin,
                            AjaxResponseMixin, View):
    """
    Update order status and go back to the order list page
    """
    raise_exception = True

    def get_ajax(self, request, *args, **kwargs):
        """
        Update order status here
        """
        status = request.GET['status']
        orders = Order.objects.filter(id__in=request.GET['ids'].split(','))
        orders.update(status=status)
        return self.render_json_response(
            {'success': True, 'new_status': Order.get_status_label(status)})
