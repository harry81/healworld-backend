# -*- coding: utf-8 -*-
import json
from main.celery_app import app as celery_app
from django.core.mail import send_mail
from core.sendsms import send_text
from constance import config
from actstream import action
from .utils import get_short_url


# @celery_app.task(bind=True)
# def send_email_healworld(self, item_title, comment):

#     send_mail(
#         u'[Healworld] 댓글입니다 %s' % item_title,
#         comment,
#         'noreply@mail.healworld.co.kr',
#         ['chharry@gmail.com',],
#         # [item.user.email],
#         fail_silently=False,
#     )


@celery_app.task(bind=True)
def send_text_healworld(self, item, comment):
    sender = '01064117846'
    comment_text = comment.comment[0:15]
    title_text = item.title

    def truncate_text(text, length):
        return text[:length] + (text[length:] and '..')

    message = u"[힐월드] '{comment}'\n\"{title}\"\n{url}".format(
        comment=truncate_text(comment_text, 15),
        title=truncate_text(title_text, 15),
        url=get_short_url("https://www.healworld.co.kr/#/detail/%s" % item.id)
    )

    phones = list(set([
        user.phone for user in item.get_comment_users(
            include_item_user=True).exclude(
            id=comment.user.id)]))

    if config.SEND_TEXT:
        response = send_text(sender, phones, message)
        result = json.dumps(response.text)

    else:
        result = send_mail(
            u"[HealWorld]SEND_TEXT 비활성화 %s" % item.title,
            u"%s to %s" % (message, phones),
            'noreply@mail.healworld.co.kr',
            ['chharry@gmail.com', ],
            fail_silently=False,
        )

    message_type = 'text' if config.SEND_TEXT else 'email'

    action.send(comment.user,
                verb='sent message via %s' % message_type,
                target=comment,
                message=message,
                result=result)
    return result
