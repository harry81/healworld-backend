# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-22 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_item_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='title',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
