# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-14 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_id',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
