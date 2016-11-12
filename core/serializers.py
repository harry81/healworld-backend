from rest_framework import serializers
from core.models import Item, Image
from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class ImageSerializer(serializers.ModelSerializer):
    itemshot = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail__100x100', 'thumbnail__100x100'),
            ('thumbnail__300x200', 'thumbnail__300x200'),
            ('thumbnail__400x400', 'thumbnail__400x400'),
        ]
    )

    class Meta:
        model = Image
        fields = ('item', 'itemshot')

class ItemSerializer(GeoFeatureModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        geo_field = "point"

        fields = ('memo', 'user', 'created_at', 'images')
