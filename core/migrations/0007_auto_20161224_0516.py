# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-24 05:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20161224_0345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='notofication_push',
            new_name='notification_push',
        ),
    ]
