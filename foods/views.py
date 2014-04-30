# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView

from braces.views import(
    AjaxResponseMixin, JSONResponseMixin
)

from .models import Food


class SearchFoodView(JSONResponseMixin, AjaxResponseMixin, FormView):
    """
    FormView for search food
    """

    def search(self, keyword):
        """
        Search the food here
        """
        return Food.objects.filter(name__contains=keyword)[:5]

    def get_ajax(self, request, *args, **kwargs):
        """
        Search API for AJAX
        """
        keyword = request.GET.get('term')
        foods = self.search(keyword) if keyword else []
        foods_json = [{'id': f.id, 'label': f.name, 'value': f.name} for f in foods]  # noqa
        return self.render_json_response(foods_json)
