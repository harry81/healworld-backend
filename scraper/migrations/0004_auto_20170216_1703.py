# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-16 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_item_core_item_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='ScraperItem',
        ),
    ]
