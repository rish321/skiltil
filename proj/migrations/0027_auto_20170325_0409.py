# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-25 04:09
from __future__ import unicode_literals

from django.db import migrations, models
import proj.models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0026_skilltopic_topic_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilltopic',
            name='topic_pic',
            field=models.ImageField(null=True, upload_to=proj.models.content_file_name),
        ),
    ]
