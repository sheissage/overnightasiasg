# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-27 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OverApp', '0007_auto_20160619_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='roominfo',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
