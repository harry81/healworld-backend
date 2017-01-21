# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django_comments.models import Comment
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D

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
        fields = ('pk', 'username', 'email', 'profile_picture_url',
                  'social_auth', 'notification_push', 'phone')


class UserSerializer(serializers.ModelSerializer):
    social_auth = UserSocialAuthForListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'username', 'profile_picture_url', 'social_auth')


class ImageSerializer(serializers.ModelSerializer):
    itemshot = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail__100x100', 'thumbnail__100x100'),
            ('thumbnail__200x200', 'thumbnail__200x200'),
            ('thumbnail__400x400', 'thumbnail__400x400'),
            ('thumbnail__1200x1200', 'thumbnail__1200x1200'),
            ('crop__400x400', 'crop__400x400'),
        ]
    )

    class Meta:
        model = Image
        fields = ('id', 'itemshot')


class ItemSerializer(GeoFeatureModelSerializer):
    image_ids = serializers.CharField(max_length=200, write_only=True)
    phone = serializers.CharField(max_length=16, write_only=True)
    images = ImageSerializer(many=True, read_only=True)
    user_id = serializers.CharField(max_length=20, write_only=True)
    user = UserSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    cnt_of_comments = serializers.SerializerMethodField()

    def get_image(self, obj):
        image = obj.images.all().order_by('id').first()

        if image:
            rlt = ImageSerializer(image).data['itemshot']['crop__400x400']
        else:
            rlt = None

        return rlt

    def get_cnt_of_comments(self, obj):
        # TODO use calculated values instead of constant
        return Comment.objects.filter(
            object_pk=obj.id, content_type=8, site_id=1).count()

    def get_distance(self, obj):
        dist = D(m=0)

        try:
            request = self.context['request']
            key = [x for x in request.GET.keys() if 'point' in x]

            if key:
                point = GEOSGeometry('POINT(%s)' %
                                     request.GET[key[0]].replace(",", " "))
                dist = D(km=obj.point.distance(point) * 100)
            else:
                return ''
        except:
            return dist

        if round(dist.km, 1) == 0:
            return "%sm" % round(dist.m, 1)

        return "%skm" % round(dist.km, 1)

    class Meta:
        model = Item
        geo_field = "point"

        fields = ('pk', 'title', 'memo', 'created_at', 'images',
                  'image_ids', 'image', 'distance',
                  'user_id', 'user', 'price', 'address', 'created_at',
                  'cnt_of_comments', 'state', 'grade', 'phone')

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        if phone:
            user = User.objects.get(id=validated_data['user_id'])
            user.phone = phone
            user.save()

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
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment

    def create(self, validated_data):
        req = self.context['request']
        user_id = req.data.get('user', None)

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                validated_data['user'] = user
            except:
                pass

        return super(CommentSerializer, self).create(validated_data)
