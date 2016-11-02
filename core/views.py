from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from core.serializers import ItemSerializer
from core.models import Item


class ItemPagination(PageNumberPagination):
    page_size = 5

class ItemAPIView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('subject', 'content',)
    pagination_class = ItemPagination

    def get_queryset(self):
        return Item.objects.order_by('-created_at')
