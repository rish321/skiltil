# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0038_auto_20161211_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
