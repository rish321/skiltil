# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-02 11:17
from __future__ import unicode_literals

from django.db import migrations, models
import proj.models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0029_skilltopic_parent_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilltopic',
            name='topic_pic',
            field=models.ImageField(default=None, null=True, upload_to=proj.models.content_file_name),
        ),
    ]