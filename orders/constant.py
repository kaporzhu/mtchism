# -*- coding: utf-8 -*-
# order status
from meals.constant import BREAKFAST, LUNCH, SUPPER


CREATED = 'created'
PAID = 'paid'
DONE = 'done'
CANCELED = 'canceled'

# deliver time
DELIVER_TIMES = {
    BREAKFAST: ['07:00-08:00', '08:00-09:00'],
    LUNCH: ['10:30-11:00',  '11:00-12:00', '12:00-12:30', '12:30-13:30'],
    SUPPER: ['17:00-17:30', '17:30-18:00', '18:00-18:30']
}
