# -*- coding: utf-8 -*-
from django import template


register = template.Library()


@register.simple_tag
def get_food_element(food, element_name, weight):
    """
    Get food element depends on the weight

    :params food: Food object
    :params element_name: Nutrient name
    :params weight: Weight in gram
    """
    amount = getattr(food, element_name)
    if amount == -1:
        return '-'
    else:
        return amount/100.0*weight
