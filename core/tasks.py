from main.celery_app import app as celery_app

@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@celery_app.task(bind=True)
def send_email_healworld(self, message):
    from django.core.mail import send_mail

    send_mail(
        message,
        'Here is the message.',
        'chharry@gmail.com',
        ['chharry@gmail.com'],
        fail_silently=False,
    )
