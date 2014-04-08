# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


def get_tomorrow():
    # if it's still earlier than 3am, we think it's yesterday
    now = datetime.now()
    if now.hour >= 0 and now.hour < 3:
        tomorrow = now
    else:
        tomorrow = datetime.now() + timedelta(days=1)

    return tomorrow
