# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-09 06:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
        ('customers', '0015_auto_20170301_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='social',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='socialaccount.SocialAccount'),
        ),
    ]