from django.core.exceptions import ObjectDoesNotExist
from django_comments.models import Comment
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer
from core.models import User, Item, Image
from social.apps.django_app.default.models import UserSocialAuth


class UserSocialAuthSerializer(serializers.ModelSerializer):
    extra_data = serializers.SerializerMethodField()

    def get_extra_data(self, obj):
        return obj.extra_data

    class Meta:
        model = UserSocialAuth


class UserSocialAuthForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAuth
        fields = ('provider', 'uid')


class ProfileSerializer(serializers.ModelSerializer):
    social_auth = UserSocialAuthSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'social_auth')


class UserSerializer(serializers.ModelSerializer):
    social_auth = UserSocialAuthForListSerializer(many=True, read_only=True)
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj):
        if obj.profile_picture.name == '':
            if obj.social_auth.all().exists():
               social = obj.social_auth.all()[0]
               if social.provider == 'facebook':
                   return 'https://graph.facebook.com/%s/picture/' % social.uid

        return obj.profile_picture.thumbnail['50x50'].url

    class Meta:
        model = User
        fields = ('pk', 'username', 'profile_picture', 'social_auth')


class ImageSerializer(serializers.ModelSerializer):
    itemshot = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail__100x100', 'thumbnail__100x100'),
            ('thumbnail__400x400', 'thumbnail__400x400'),
            ('crop__400x400', 'crop__400x400'),
        ]
    )

    class Meta:
        model = Image
        fields = ('id', 'itemshot')


class ItemSerializer(GeoFeatureModelSerializer):
    image_ids = serializers.CharField(max_length=200, write_only=True)
    images = ImageSerializer(many=True, read_only=True)
    user_id = serializers.CharField(max_length=20, write_only=True)
    user = UserSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    cnt_of_comments = serializers.SerializerMethodField()

    def get_image(self, obj):
        image = obj.images.all().order_by('created_at').first()

        if image:
            rlt = ImageSerializer(image).data['itemshot']['crop__400x400']
        else:
            rlt = None

        return rlt

    def get_cnt_of_comments(self, obj):
        # TODO use calculated values instead of constant
        return Comment.objects.filter(
            object_pk=obj.id, content_type=8, site_id=1).count()

    class Meta:
        model = Item
        geo_field = "point"

        fields = ('pk', 'title', 'memo', 'created_at', 'images', 'image_ids', 'image',
                  'user_id', 'user', 'price', 'address', 'created_at',
                  'cnt_of_comments')

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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
