# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='paytm_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='gmail_id',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='skype_id',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
