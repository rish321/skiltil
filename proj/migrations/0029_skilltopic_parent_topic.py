# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-02 09:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0028_skill_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='skilltopic',
            name='parent_topic',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='proj.SkillTopic'),
        ),
    ]