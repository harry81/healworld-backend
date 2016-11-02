from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from core import views as core_views

router = routers.SimpleRouter()
router.register(r'api-core', core_views.ItemAPIView, base_name="api-core")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
