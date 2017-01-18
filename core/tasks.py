# -*- coding: utf-8 -*-
from main.celery_app import app as celery_app
from django.core.mail import send_mail
from core.sendsms import send_text
from constance import config


@celery_app.task(bind=True)
def send_email_healworld(self, comment):

    item = comment.content_type.get_all_objects_for_this_type().get(
        id=comment.object_pk)

    send_mail(
        u'[Healworld] 댓글입니다 %s' % item.title,
        comment.comment,
        'noreply@mail.healworld.co.kr',
        [item.user.email],
        fail_silently=False,
    )


@celery_app.task(bind=True)
def send_text_healworld(self, comment):
    sender = '01064117846'
    receivers = ['01064117846', ]

    if config.SEND_TEXT:
        send_text(sender, receivers, comment.comment)
    else:
        send_mail(
            u'[Healworld] 댓글입니다, SEND_TEXT 비활성화',
            u'SEND_TEXT 비활성화로 문자 대신 메일로 전송',
            'noreply@mail.healworld.co.kr',
            ['chharry@gmail.com'],
            fail_silently=False,
        )
