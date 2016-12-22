# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-22 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0039_auto_20161212_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='call',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='session',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
