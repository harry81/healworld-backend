from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from core.serializers import ItemSerializer, ImageSerializer
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework_gis.filters import DistanceToPointFilter
from core.models import Item, Image
from rest_framework import generics


class ItemPagination(PageNumberPagination):
    page_size = 5


class ItemAPIView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    pagination_class = ItemPagination
    filter_backends = (filters.SearchFilter,)

    distance_filter_field = 'point'
    filter_backends = (DistanceToPointFilter, )
    bbox_filter_include_overlapping = True # Optional

    def get_queryset(self):
        return Item.objects.order_by('-created_at')


class ImageAPIView(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        return self.get_queryset.order_by('-created_at')
