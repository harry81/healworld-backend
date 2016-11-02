from __future__ import unicode_literals

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.text)


class Image(models.Model):
    image = models.CharField(max_length=256, blank=False)
    created_at = models.DateTimeField(db_index=True,
                                      default=timezone.now, blank=True)
    post = models.ForeignKey(Item,
                             on_delete=models.CASCADE,
                             related_name='images')

    def __unicode__(self):
        return u'%s %s' % (self.image, self.post.subject)
