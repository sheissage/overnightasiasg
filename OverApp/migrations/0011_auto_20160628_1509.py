# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-28 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OverApp', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelavailability',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]