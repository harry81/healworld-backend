from __future__ import unicode_literals

from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.gis.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
from django.utils.translation import ugettext_lazy as _


class Item(models.Model):
    memo = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True)
    price = models.IntegerField(default=1000)
    point = models.PointField(verbose_name=_("Item location"),
                              blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.text)


class Image(models.Model):
    item = models.ForeignKey(Item,
                             on_delete=models.CASCADE,
                             related_name='images')
    itemshot = VersatileImageField('Item',
                                   blank=True,
                                   null=True,
                                   upload_to='items/',
                                   ppoi_field='item_ppoi'
    )
    item_ppoi = PPOIField()
    created_at = models.DateTimeField(db_index=True,
                                      default=timezone.now, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.id, self.itemshot)
