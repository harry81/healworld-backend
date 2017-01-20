# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


def time_to_send_text():
    now = datetime.now()

    if now.hour > 21:
        eta = (now + timedelta(days=1)).replace(hour=8, minute=10)
    else:
        eta = now + timedelta(hours=1)

    return eta
