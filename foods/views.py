# -*- coding: utf-8 -*-
import json

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView

from .forms import UploadFoodForm
from .models import Category, Food


class UploadFoodView(FormView):
    """
    FormView for uploading food data to the server.
    The food  data should be a JSON file.
    JSON FORMATION:

        [
            {
                'name': 'food name',
                'category_name': 'food category name',
                'heat': 20.1,
                'carbohydrate': 3.3,
                'fat': 2.4,
                'protein': 2.11,
                'cellulose': 0.1
            },
            ...
        ]

    If food name
        existed: update the other fields.
        not existed: add a new one.
    If food category name doesn't exist, create a new category.
    """
    form_class = UploadFoodForm
    template_name = 'foods/upload.html'
    success_url = reverse_lazy('foods:upload')
    required_fields = ['name', 'category_name', 'heat', 'carbohydrate', 'fat',
                       'protein', 'cellulose']

    def form_valid(self, form):
        """
        Process food data in JSON file.

        Result formation

            {
                'category_name':
                {
                    'created': True,
                    'added': 10,
                    'updated': 1
                }
            }
        """
        # upload result
        result = {}
        failed_items = []

        foods = form.cleaned_data['foods']  # JSON data from the uploaded file
        for fd in foods:
            if sorted(fd.keys()) == sorted(self.required_fields):
                category, cat_created = Category.objects.get_or_create(name=fd['category_name'])  # noqa
                food, food_created = Food.objects.get_or_create(
                    name=fd['name'], category = category)
                food.heat = fd['heat']
                food.carbohydrate = fd['carbohydrate']
                food.fat = fd['fat']
                food.protein = fd['protein']
                food.cellulose = fd['cellulose']
                food.save()

                # update result
                rst = result.get(category.name, {})
                rst['created'] = rst.get('created', cat_created)
                if food_created:
                    rst['added'] = rst.get('added', 0) + 1
                else:
                    rst['updated'] = rst.get('updated', 0) + 1
                result[category.name] = rst
            else:
                failed_items.append(fd)

        # user message
        for cat_name, rst in result.iteritems():
            msg = u'{}({}): {} added, {} updated'.format(
                cat_name, 'Created' if rst['created'] else 'Updated',
                rst.get('added', 0), rst.get('updated', 0))
            messages.success(self.request, msg)

        if failed_items:
            failed_msg = json.dumps(failed_items, indent=4, ensure_ascii=False,
                                    encoding='utf8')
            failed_msg = failed_msg.replace('\n', '<br/>').replace('    ', '&nbsp;'*4)  # noqa
            messages.warning(self.request, failed_msg)

        return super(UploadFoodView, self).form_valid(form)
