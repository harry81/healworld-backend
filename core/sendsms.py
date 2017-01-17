# -*- coding: utf-8 -*-
import base64
import httplib
import json

from django.conf import settings

appid = settings.SMS_APPID
apikey = settings.SMS_APIKEY
address = 'api.bluehouselab.com'

credential = "Basic "+base64.encodestring(appid+':'+apikey).strip()
headers = {
    "Content-type": "application/json;charset=utf-8",
    "Authorization": credential,
}

c = httplib.HTTPSConnection(address)

path = "/smscenter/v1.0/send%s"


def send_text(sender, receivers, content):
    value = {
        'sender': sender,
        'receivers': receivers,
        'subject': u'LMS 제목',
        'content': content,
    }

    data = json.dumps(value, ensure_ascii=False).encode('utf-8')

    c.request("POST", path % 'sms', data, headers)
    ret = c.getresponse()
    return ret
