# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-26 04:04
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_item_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='state',
            field=django_fsm.FSMField(default='created', max_length=50),
        ),
    ]
