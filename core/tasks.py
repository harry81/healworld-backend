from main.celery_app import app as celery_app

@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
