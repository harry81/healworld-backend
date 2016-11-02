from rest_framework import serializers
from core.models import Item, Image

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('text', 'user', 'created_at')
