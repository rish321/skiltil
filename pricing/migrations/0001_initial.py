# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-02 09:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PriceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('fixed_price', models.IntegerField(default=0)),
                ('fixed_price_time_end', models.DurationField(default=datetime.timedelta)),
                ('red_cost_factor', models.FloatField(default=0)),
                ('red_cost_time_end', models.DurationField(default=datetime.timedelta)),
                ('cost_factor', models.FloatField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]