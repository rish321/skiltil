# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0005_skill_image_src'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='details',
            field=models.TextField(default=b''),
        ),
    ]
