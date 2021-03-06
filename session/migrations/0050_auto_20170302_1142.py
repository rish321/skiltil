# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-02 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0049_auto_20170302_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='student_pricing',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_pricing', to='pricing.PriceModel'),
        ),
        migrations.AlterField(
            model_name='session',
            name='teacher_pricing',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_pricing', to='pricing.PriceModel'),
        ),
    ]
