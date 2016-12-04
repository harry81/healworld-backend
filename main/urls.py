from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from core import views as core_views

router = routers.SimpleRouter()
router.register(r'api-item', core_views.ItemAPIView, base_name="api-item")
router.register(r'api-image', core_views.ImageAPIView, base_name="api-image")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^get_host$', core_views.get_host, name='get_host'),
]
