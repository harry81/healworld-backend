# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django_comments.models import Comment

from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import list_route
from core.serializers import (ItemSerializer, ImageSerializer,
                              CommentSerializer, ProfileSerializer)
from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework_jwt.settings import api_settings
from core.models import Item, User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_token(request):
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

    host = request.META['HTTP_HOST'].replace('backend', 'www')

    html = "<meta http-equiv=\"refresh\" content=\"0; \
URL='%s://%s'\" />" % (request.META['wsgi.url_scheme'],
                       host)

    response = HttpResponse(html)

    response.set_cookie('jwt_token', token,
                        domain=settings.SESSION_COOKIE_DOMAIN)
    response.set_cookie('username', user.username,
                        domain=settings.SESSION_COOKIE_DOMAIN)
    response.set_cookie('provider', provider,
                        domain=settings.SESSION_COOKIE_DOMAIN)
    return response


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


class ProfileAPIView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    @list_route()
    def info(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
