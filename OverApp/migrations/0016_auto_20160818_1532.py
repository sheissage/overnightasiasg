# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-18 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OverApp', '0015_hotelinfo_airporttransfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OverApp.Traveller'),
        ),
    ]
