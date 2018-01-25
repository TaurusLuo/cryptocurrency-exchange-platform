# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-23 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20180112_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='wallet',
            name='words',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
