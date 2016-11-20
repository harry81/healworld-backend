from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
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
        fields = ('id', 'itemshot')


class ItemSerializer(GeoFeatureModelSerializer):
    image_ids = serializers.CharField(max_length=200, write_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        geo_field = "point"

        fields = ('memo', 'user', 'created_at', 'images', 'image_ids')

    def create(self, validated_data):
        image_ids = validated_data.pop('image_ids')
        item = super(ItemSerializer, self).create(validated_data)

        for image_id in image_ids.split(','):
            try:
                image = Image.objects.get(id=image_id)
                item.images.add(image)

            except ObjectDoesNotExist:
                pass

        return item
