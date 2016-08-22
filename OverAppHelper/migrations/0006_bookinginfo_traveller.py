# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-31 06:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OverApp', '0015_hotelinfo_airporttransfer'),
        ('OverAppHelper', '0005_auto_20160715_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinginfo',
            name='traveller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='OverApp.Traveller'),
            preserve_default=False,
        ),
    ]
