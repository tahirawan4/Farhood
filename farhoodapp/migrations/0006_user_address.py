# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farhoodapp', '0005_event_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
