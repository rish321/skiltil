# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-01 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0021_skill_pre_requisites'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='skill_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='skill_rating_count',
            field=models.IntegerField(default=0),
        ),
    ]
