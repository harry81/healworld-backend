# -*- coding: utf-8 -*-
from main.celery_app import app as celery_app
from django.core.mail import send_mail
from core.sendsms import send_text
from constance import config
from actstream import action


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

    phones = list(set([
        user.phone for user in item.get_comment_users().exclude(
            id=comment.user.id)]))

    if config.SEND_TEXT:
        send_text(sender, phones, message)

    else:
        send_mail(
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
                message=message)
