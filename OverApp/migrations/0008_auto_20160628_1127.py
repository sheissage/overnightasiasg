# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-28 11:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OverApp', '0007_auto_20160619_0651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('picture', models.ImageField(upload_to='Gallery/')),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OverApp.HotelInfo')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OverApp.RoomInfo')),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Gallery',
            },
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
