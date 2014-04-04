# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin, JSONResponseMixin

from .constant import CANCELED
from .forms import CheckoutForm
from .models import Order, OrderMeal
from meals.models import Meal


class CheckoutView(LoginRequiredMixin, JSONResponseMixin, FormView):
    """
    View for checkout the meals
    """
    template_name = 'orders/checkout.html'
    form_class = CheckoutForm

    def form_valid(self, form):
        """
        Create order here
        """
        data = form.cleaned_data
        order = Order(creator=self.request.user, address=data['address'])
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
        context = {'success': True, 'success_url': '/'}
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
