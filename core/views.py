from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from core.serializers import ItemSerializer, ImageSerializer, CommentSerializer
from rest_framework_gis.filters import DistanceToPointFilter
from core.models import Item
from django_comments.models import Comment
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def social_complete(request):
    user = request.user
    try:
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

    except AttributeError:
        token = None

    try:
        provider = user.social_auth.all()[0].provider
    except:
        provider = None

    info = JsonResponse({
        'username': user.username,
        'token': token,
        'provider': provider,
    })

    return info


class ItemPagination(PageNumberPagination):
    page_size = 10


class ItemAPIView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    pagination_class = ItemPagination

    distance_filter_field = 'point'
    filter_backends = (DistanceToPointFilter, filters.SearchFilter)
    bbox_filter_include_overlapping = True  # Optional
    distance_filter_convert_meters = True
    search_fields = ('memo', )

    def get_queryset(self):
        return Item.objects.order_by('-created_at')


class ImageAPIView(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        return self.get_queryset.order_by('-created_at')


class CommentAPIView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('object_pk', )
    ordering = ('-submit_date',)

    def get_queryset(self):
        return Comment.objects.order_by('-submit_date')
