# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-08 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OverApp', '0012_auto_20160708_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelinfo',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
