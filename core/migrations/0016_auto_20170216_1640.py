# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-16 07:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='link',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]