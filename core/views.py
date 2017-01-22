# -*- coding: utf-8 -*-
import json
import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django_comments.models import Comment

from rest_framework import viewsets, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from core.serializers import (ItemSerializer, ImageSerializer,
                              CommentSerializer, ProfileSerializer)
from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework_jwt.settings import api_settings
from core.models import Item, User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_token(request):
    user = request.user

    host = request.META['HTTP_HOST'].replace(
        'backend', 'www').replace('8000', '8100')
    html = "<meta http-equiv=\"refresh\" content=\"0; \
URL='%s://%s'\" />" % (request.META['wsgi.url_scheme'],
                       host)

    response = HttpResponse(html)

    try:
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        expires = datetime.datetime.strftime(
            datetime.datetime.utcnow() +
            datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE),
            "%a, %d-%b-%Y %H:%M:%S GMT")

        response.set_cookie('jwt_token', token,
                            domain=settings.SESSION_COOKIE_DOMAIN,
                            expires=expires)
    except AttributeError:
        pass

    return response


def show_api_settings(request):
    from rest_framework_jwt.settings import api_settings
    jwt_value = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')

    payload = api_settings.JWT_DECODE_HANDLER(jwt_value)
    html = "%s<br>%s" % (api_settings.defaults.items(), payload)
    response = HttpResponse(html)
    return response


class ItemPagination(PageNumberPagination):
    page_size = 10


class ItemAPIView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    pagination_class = ItemPagination

    distance_filter_field = 'point'
    filter_backends = (DistanceToPointFilter,
                       filters.SearchFilter, DjangoFilterBackend)
    bbox_filter_include_overlapping = True  # Optional
    distance_filter_convert_meters = True
    search_fields = ('memo', 'title')
    filter_fields = ('state', 'user')

    def get_queryset(self):
        return Item.live_objects.order_by('-created_at')

    @detail_route(methods=['patch'])
    def state_action(self, request, pk):
        # TODO : check the permission

        action = request.GET['action']
        if action not in ['going', 'complete']:
            return Response("Action [ %s ] not defined" % action,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return Response("Item is not exists[%s]" % pk,
                            status=status.HTTP_400_BAD_REQUEST)

        methodToCall = getattr(item, action)
        methodToCall()
        item.save()

        return Response('%s' % action, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        response = super(ItemAPIView, self).list(request, args, kwargs)
        response.data['request_query'] = dict(request.GET)
        return response

    def patch(self, request):
        data_obj = json.loads(json.dumps(request.data))
        item_id = data_obj.pop('item_id')

        try:
            user = request.user
            item = Item.objects.get(id=item_id, user=user)
            item.__dict__.update(**data_obj)
            item.save()

        except Item.DoesNotExist:
            ret = {'result': '%s not exist' % item_id}
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

        ret = {'result': '%s deleted' % item_id}
        return Response(ret, status=status.HTTP_200_OK)


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

    @list_route()
    def logout(self, request):
        request.session.flush()
        logout(request)
        return Response({'logout': "ok"}, status=status.HTTP_200_OK)

    def patch(self, request):
        data_obj = json.loads(json.dumps(request.data))

        if 'notification_push' in data_obj:
            data_obj['notification_push'] =\
                data_obj['notification_push'].split('/')[-1].strip("'")

        user = request.user
        user.__dict__.update(**data_obj)
        user.save()

        ret = {'result': '%s patched' % user.id, 'data': data_obj}
        return Response(ret, status=status.HTTP_200_OK)
