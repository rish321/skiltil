# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-26 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0011_customer_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
