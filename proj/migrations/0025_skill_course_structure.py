# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-07 07:24
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0024_auto_20170304_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='course_structure',
            field=tinymce.models.HTMLField(blank=True, default=b''),
        ),
    ]
