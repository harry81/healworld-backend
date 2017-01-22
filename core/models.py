from __future__ import unicode_literals

import requests
import json
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_comments.models import Comment

from django_fsm import FSMField, transition
from versatileimagefield.fields import VersatileImageField, PPOIField
from django.utils.translation import ugettext_lazy as _
from .tasks import send_text_healworld
from .utils import time_to_send_text


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    notification_push = models.CharField(max_length=512, blank=True,
                                         null=True, default=True)

    profile_picture = VersatileImageField('User Profile',
                                          blank=True,
                                          null=True,
                                          upload_to='user_profile/')
    profile_picture_url = models.CharField(max_length=512, blank=True,
                                           null=True, default='')
    phone = models.CharField(max_length=32, blank=True,
                             null=True, default=None)

    def send_push_notification(self):
        if self.notification_push is not None:

            url = "https://android.googleapis.com/gcm/send"
            headers = {"Authorization": 'key=%s' % settings.GCM_SERVER_KEY,
                       "Content-Type": "application/json"}
            payload = {
                "registration_ids": [self.notification_push],
                "data": {"title": "title",
                         "body": "body",
                         "color": "red"}
            }

            requests.post(url, data=json.dumps(payload), headers=headers)

    def update_picture_url(self):
        image_url = '/assets/imgs/person.png'

        if self.profile_picture.name == '':
            if self.social_auth.all().exists():
                social = self.social_auth.all()[0]

                if social.provider == 'facebook':
                    image_url = 'https://graph.facebook.com/%s/picture/'\
                                % social.uid

                elif social.provider == 'kakao':
                    res = requests.get(
                        'https://kapi.kakao.com/v1/api/talk/profile',
                        headers={'Authorization': 'Bearer %s'
                                 % social.access_token})
                    res_json = json.loads(res.content)
                    image_url = res_json['thumbnailURL']

                elif social.provider == 'naver':
                    res = requests.get(
                        'https://openapi.naver.com/v1/nid/me',
                        headers={'Authorization': 'Bearer %s'
                                 % social.access_token})
                    res_json = json.loads(res.content)
                    image_url = res_json['response']['profile_image']

                    social.extra_data['respose'] = res_json['response']
                    social.save()

        else:
            image_url = self.profile_picture.thumbnail['50x50'].url

        self.profile_picture_url = image_url
        self.save()

    def __unicode__(self):
        return u'%s' % (self.username)


class ItemManager(models.Manager):
    def get_queryset(self):
        return super(ItemManager, self).get_queryset().filter(deleted=False)


class Item(models.Model):
    title = models.CharField(max_length=512, blank=True, null=True)
    memo = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True)
    price = models.IntegerField(default=1000)
    grade = models.IntegerField(default=3)
    point = models.PointField(verbose_name=_("Item location"),
                              blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    state = FSMField(default='created', protected=True)
    deleted = models.BooleanField(default=False)
    objects = models.Manager()
    live_objects = ItemManager()

    def __unicode__(self):
        return u'%s' % (self.title)

    def get_comment_users(self):
        comments = Comment.objects.filter(
            content_type=ContentType.objects.get(model='item'),
            object_pk=self.pk)
        users = set([
            ele.user.id for ele in comments.exclude(
                user=None).distinct()])

        return User.objects.filter(id__in=users)

    @transition(field=state, source=['created', 'ongoing'],
                target='completed', custom=dict(admin=True))
    def complete(self):
        pass

    @transition(field=state, source='created', target='ongoing')
    def going(self):
        pass


class Image(models.Model):
    item = models.ForeignKey(Item,
                             on_delete=models.CASCADE,
                             null=True,
                             related_name='images')
    itemshot = VersatileImageField('Item',
                                   blank=True,
                                   null=True,
                                   upload_to='items/',
                                   ppoi_field='item_ppoi')

    item_ppoi = PPOIField()
    created_at = models.DateTimeField(db_index=True,
                                      default=timezone.now, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.id, self.itemshot)


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, created, **kwargs):
    if not created:  # do nothing if it's not new comment
        return

    comment = instance

    item = comment.content_type.get_all_objects_for_this_type().get(
        id=comment.object_pk)
    users = item.get_comment_users()

    for user in User.objects.filter(id__in=users).exclude(id=comment.user.id):
        user.send_push_notification()

    eta = time_to_send_text()

    item = comment.content_type.get_all_objects_for_this_type().get(
        id=comment.object_pk)

    # send_email_healworld.apply_async((comment,), eta=eta)
    send_text_healworld.apply_async((item, comment,), eta=eta)
