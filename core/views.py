from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from core.serializers import ItemSerializer, ImageSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework_gis.filters import DistanceToPointFilter
from core.models import Item, Image
from rest_framework import generics
from django_comments.models import Comment


class ItemPagination(PageNumberPagination):
    page_size = 10

class ItemAPIView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    pagination_class = ItemPagination

    distance_filter_field = 'point'
    filter_backends = (DistanceToPointFilter, filters.SearchFilter)
    bbox_filter_include_overlapping = True # Optional
    search_fields = ('memo', )

    def get_queryset(self):
        return Item.objects.order_by('-created_at')


class ImageAPIView(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        return self.get_queryset.order_by('-created_at')


class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('object_pk', )
    ordering = ('-submit_date',)
