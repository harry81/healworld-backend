from __future__ import unicode_literals
from django.db import models


class Item(models.Model):
    item_id = models.CharField(max_length=64, unique=True)
    from_id = models.CharField(max_length=64, blank=True, null=True)
    from_name = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    item_type = models.CharField(max_length=16, blank=True, null=True)
    link = models.CharField(max_length=512, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.name)
