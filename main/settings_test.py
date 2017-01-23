try:
    from settings import *
except:
    pass


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
