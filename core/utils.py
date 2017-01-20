# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from constance import config


def time_to_send_text():
    now = datetime.utcnow()

    if now.hour > 21:
        eta = (now + timedelta(days=1)).replace(hour=8, minute=10)
    else:
        eta = now + timedelta(seconds=config.SECONDS_TO_SEND_TEXT)

    return eta
