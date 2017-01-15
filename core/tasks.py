# -*- coding: utf-8 -*-

from main.celery_app import app as celery_app


@celery_app.task(bind=True)
def send_email_healworld(self, comment):
    from django.core.mail import send_mail

    item = comment.content_type.get_all_objects_for_this_type().get(
        id=comment.object_pk)

    send_mail(
        u'신규 댓글',
        comment.comment,
        'chharry@gmail.com',
        [item.user.email],
        fail_silently=False,
    )
