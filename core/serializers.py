from rest_framework import serializers
from core.models import Item, Image
from versatileimagefield.serializers import VersatileImageFieldSerializer

class ImageSerializer(serializers.ModelSerializer):
    itemshot = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )

    class Meta:
        model = Image
        fields = ('item', 'itemshot')

class ItemSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('text', 'user', 'created_at', 'images')
