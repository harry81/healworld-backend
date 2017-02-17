# -*- coding: utf-8 -*-
import json
from main.celery_app import app as celery_app
from django.core.mail import send_mail, EmailMessage
from core.sendsms import send_text
from constance import config
from actstream import action
from celery.utils.log import get_task_logger
from .utils import get_short_url, get_reports
from scraper.facebook.get_fb_posts_fb_group import (
    scrapeFacebookPageFeedStatus,
    copyStatusToCore)

logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def scrap_facebook(self,  **kwargs):
    for group_id in kwargs['group_ids']:
        scrapeFacebookPageFeedStatus(group_id)

    # TODO : send report email


@celery_app.task(bind=True)
def copy_scraped_facebook(self):
    copyStatusToCore()


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


@celery_app.task(bind=True)
def send_reports(self):
    report = get_reports()
    message = ""

    for k, v in report.items():
        message = message + "%s : %s<br>" % (k, v)

    msg = EmailMessage(
        u"daily report",
        message,
        'noreply@mail.healworld.co.kr',
        ['chharry@gmail.com', ]
    )
    msg.content_subtype = "html"
    msg.send()


@celery_app.task(bind=True)
def test_send_mail(self):
    title = "test_send_mail"
    message = "test"

    send_mail(
        title,
        message,
        'noreply@mail.healworld.co.kr',
        ['chharry@gmail.com', ],
        fail_silently=False,
    )
    logger.info("Start task")
