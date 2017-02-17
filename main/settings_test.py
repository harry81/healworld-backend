try:
    from settings import *
except:
    pass


CELERY_ALWAYS_EAGER = True
TEST_RUNNER = 'core.test_runner.TestRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'db_healworld_test',
        'USER': 'healworld',
        'PASSWORD': 'easypassword',
        'HOST': 'localhost',
        'PORT': '5432'
    }
 }
