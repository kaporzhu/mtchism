# -*- coding: utf-8 -*-
import collections
import json
from datetime import datetime

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

from .constant import CANCELED, DELIVER_TIMES, PAID
from .forms import CheckoutForm
from .models import Order, OrderMeal
from .utils import get_tomorrow
from buildings.models import Building
from meals.constant import BREAKFAST, SUPPER, LUNCH, OTHER
from meals.models import Meal
from mtchism.mixins import PaginationMixin
from plans.models import UserPlan, StageMeal, UserStageDay


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
                     'deliver_times': collections.OrderedDict(sorted(DELIVER_TIMES.items())),  # noqa
                     'meal_type_choices': Meal.MEAL_TYPE_CHOICES,
                     'tomorrow': get_tomorrow()})
        data.update(self.request.GET.items())
        return data

    def form_valid(self, form):
        """
        Create order here
        """
        data = form.cleaned_data
        location = data['location']
        deliver_times = {
            BREAKFAST: data.get('breakfast_deliver_time'),
            LUNCH: data.get('lunch_deliver_time'),
            SUPPER: data.get('supper_deliver_time'),
            OTHER: None
        }
        building = Building.objects.get(pk=data['building'])

        # update user address and preferred time
        profile = self.request.user.profile
        profile.building = building
        profile.location = location
        for tp, time in deliver_times.iteritems():
            if time:
                setattr(profile, 'preferred_{}_time'.format(tp), time)
        profile.save()

        # create order
        order = Order(creator=self.request.user, location=location,
                      building=building,
                      breakfast_deliver_time=deliver_times[BREAKFAST],
                      lunch_deliver_time=deliver_times[LUNCH],
                      supper_deliver_time=deliver_times[SUPPER],
                      deliver_date=get_tomorrow())
        order.save()
        total_price = 0
        total_amount = 0

        if 'stage_meals' == self.request.GET.get('type'):
            user_plan = UserPlan.objects.get(pk=self.request.GET['userplan'])
            stage_day = UserStageDay(user=self.request.user,
                                     user_stage=user_plan.current_stage,
                                     order=order,
                                     date=order.deliver_date)
            stage_day.save()
            user_plan.validate()
            for stage_meal_info in data['meals']:
                stage_meal = StageMeal.objects.get(pk=stage_meal_info['id'])
                stage_day.meals.add(stage_meal)
                deliver_time = deliver_times[stage_meal_info['meal_type']]
                total_price += stage_meal.meal.price
                total_amount += 1
                order_meal = OrderMeal(meal=stage_meal.meal,
                                       creator=self.request.user,
                                       order=order,
                                       amount=1,
                                       meal_type=stage_meal_info['meal_type'])
                if deliver_time:
                    order_meal.deliver_time = deliver_time
                order_meal.save()

        else:
            for meal_info in data['meals']:
                amount = meal_info['amount']
                meal = Meal.objects.get(pk=meal_info['id'])
                deliver_time = deliver_times[meal_info['meal_type']]
                total_price += meal.price * amount
                total_amount += amount
                order_meal = OrderMeal(meal=meal,
                                       creator=self.request.user,
                                       order=order,
                                       amount=meal_info['amount'],
                                       meal_type=meal_info['meal_type'],
                                       deliver_time=deliver_time)
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
        orders = Order.objects.filter(
            creator=self.request.user).order_by('-deliver_date')[:30]
        orders_tomorrow = []
        orders_today = []
        order_yesterday = []
        today = datetime.now().date()
        for order in orders:
            interval = (today-order.deliver_date).days
            if interval == -1:
                orders_tomorrow.append(order)
            elif interval == 0:
                orders_today.append(order)
            elif interval == 1:
                order_yesterday.append(order)
            else:
                break

        my_orders = [{'label': u'明天', 'orders': orders_tomorrow},
                     {'label': u'今天', 'orders': orders_today},
                     {'label': u'昨天', 'orders': order_yesterday}]
        data.update({'my_orders': my_orders})
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


class OrderListView(StaffuserRequiredMixin, PaginationMixin, ListView):
    """
    Display all the orders for the staff
    """
    model = Order
    paginate_by = 15

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

        # deliver time
        meal_type = params['meal_type']
        deliver_time = params['deliver_time']
        if meal_type == BREAKFAST:
            deliver_time_Q = Q(breakfast_deliver_time=deliver_time) if deliver_time != 'all' else ~Q(breakfast_deliver_time__exact='')  # noqa
        elif meal_type == LUNCH:
            deliver_time_Q = Q(lunch_deliver_time=deliver_time) if deliver_time != 'all' else ~Q(lunch_deliver_time__exact='')  # noqa
        elif meal_type == SUPPER:
            deliver_time_Q = Q(supper_deliver_time=deliver_time) if deliver_time != 'all' else ~Q(supper_deliver_time__exact='')  # noqa
        else:
            deliver_time_Q = Q()

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

        return qs.filter(status_Q, building_Q, deliver_time_Q, location_Q,
                         created_time_Q)

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(OrderListView, self).get_context_data(**kwargs)
        data.update({'status_choices': Order.STATUS_CHOICES,
                     'buildings': Building.objects.filter(is_active=True),
                     'meal_type_choices': Meal.MEAL_TYPE_CHOICES,
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


class PayView(LoginRequiredMixin, RedirectView):
    """
    Fake payment view.
    Simply set the order to paid.
    """
    permanent = False

    def get(self, request, *args, **kwargs):
        """
        Update order status here.
        """
        order = Order.objects.get(pk=kwargs['pk'], creator=request.user)
        order.status = PAID
        order.save()
        return redirect(reverse('orders:mine'))
