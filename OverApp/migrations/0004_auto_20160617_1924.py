# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-17 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OverApp', '0003_hotelavailability_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelavailability',
            name='currency',
        ),
        migrations.AddField(
            model_name='hotelinfo',
            name='currency',
            field=models.CharField(default='USD', max_length=3),
        ),
    ]
