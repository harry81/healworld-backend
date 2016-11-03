from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from core.serializers import ItemSerializer, ImageSerializer
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from core.models import Item, Image


class ItemPagination(PageNumberPagination):
    page_size = 5


class ItemAPIView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = ItemPagination

    def get_queryset(self):
        return Item.objects.order_by('-created_at')


class ImageAPIView(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.order_by('-created_at')

    def put(self, request, format=None):
        file_obj = request.data['file']
        item_id = request.POST.get('item_id')
        image = Image.objects.create(item_id=item_id, itemshot=file_obj)

        data = {
            "item_id": item_id,
            "image_id": image.id
        }
        print data
        return Response(status=201, data=data)
