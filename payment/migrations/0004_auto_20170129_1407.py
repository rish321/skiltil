# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-29 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20161222_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='mode',
            field=models.CharField(choices=[('paytm', 'Paytm'), ('account', 'Account Transfer'), ('cash', 'Cash'), ('other', 'Others')], default='paytm', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payout',
            name='mode',
            field=models.CharField(choices=[('paytm', 'Paytm'), ('account', 'Account Transfer'), ('cash', 'Cash'), ('other', 'Others')], default='paytm', max_length=20),
        ),
        migrations.AddField(
            model_name='payout',
            name='transaction_id',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
