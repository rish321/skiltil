# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 18:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0033_auto_20161211_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, 0, 279218, tzinfo=utc)),
        ),
    ]
