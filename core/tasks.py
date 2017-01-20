# -*- coding: utf-8 -*-
from main.celery_app import app as celery_app
from django.core.mail import send_mail
from core.sendsms import send_text
from constance import config


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

    message = u"[HealWorld]신규 댓글-'%s' - %s" % (
        item.title[:20], comment.comment[0:20])

    for user in item.get_comment_users():
        if config.SEND_TEXT and user.phone:
            send_text(sender, [user.phone, ], message)

        else:
            send_mail(
                u"[HealWorld]SEND_TEXT 비활성화 %s" % item.title,
                u"%s" % message,
                'noreply@mail.healworld.co.kr',
                ['chharry@gmail.com', ],
                fail_silently=False,
            )
