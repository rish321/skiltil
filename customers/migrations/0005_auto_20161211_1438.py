# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_skillmatch_classes_given'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='wallet_amount',
            field=models.FloatField(default=0),
        ),
    ]