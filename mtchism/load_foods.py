# -*- coding: utf-8 -*-
import json
import os
import re
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtchism.settings')


from foods.models import Category, Food


with open('boohee_2014_04_29_18_51_17.json') as data_file:
    for line in data_file.readlines():
        fd = json.loads(line.strip('[],\n\r'))
        category, cat_created = Category.objects.get_or_create(
                    name=fd['category_name'])
        origin_id = int(re.match('.*shiwu/(\d*)', fd['url']).group(1))
        try:
            food = Food.objects.get(origin_id=origin_id)
            created = False
        except Food.DoesNotExist:
            food = Food(name=fd['name'], category=category)
            created = True

        food.origin_id = origin_id
        food.heat = fd['heat']
        food.carbohydrate = fd['carbohydrate']
        food.fat = fd['fat']
        food.protein = fd['protein']
        food.cellulose = fd['cellulose']
        food.url = fd['url']
        food.image_url = fd.get('image_url')
        food.save()
