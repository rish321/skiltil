# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0008_skilltopic_clicks'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='classes_given',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skilltopic',
            name='classes_given',
            field=models.IntegerField(default=0),
        ),
    ]
