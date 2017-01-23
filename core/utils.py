# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
import requests
from constance import config
from django.conf import settings


def time_to_send_text():
    now = datetime.utcnow()

    if now.hour > 21:
        eta = (now + timedelta(days=1)).replace(hour=8, minute=10)
    else:
        eta = now + timedelta(seconds=config.SECONDS_TO_SEND_TEXT)

    return eta


def get_short_url(long_url):
    api_url = "https://openapi.naver.com/v1/util/shorturl"

    payload = {
        'url': long_url
    }

    headers = {
        "X-Naver-Client-Id": settings.SOCIAL_AUTH_NAVER_KEY,
        "X-Naver-Client-Secret": settings.SOCIAL_AUTH_NAVER_SECRET
    }

    response = requests.post(api_url, data=payload, headers=headers)
    res_json = json.loads(response.text)
    return res_json['result']['url']
