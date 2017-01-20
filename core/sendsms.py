# -*- coding: utf-8 -*-
import base64
import json
import requests

from django.conf import settings

appid = settings.SMS_APPID
apikey = settings.SMS_APIKEY
address = 'api.bluehouselab.com'

credential = "Basic "+base64.encodestring(appid+':'+apikey).strip()
headers = {
    "Content-type": "application/json;charset=utf-8",
    "Authorization": credential,
}

url = 'https://api.bluehouselab.com/smscenter/v1.0/sendsms'


def send_text(sender, receivers, content):
    headers = {'Content-type': 'application/json; charset=utf-8'}
    params = {
        'sender': sender,
        'receivers': receivers,
        'content': content,
    }
    requests.post(url, data=json.dumps(params),
                  auth=(appid, apikey), headers=headers)
