# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-11 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('OverApp', '0013_auto_20160708_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('days', models.IntegerField()),
                ('checkin', models.IntegerField()),
                ('checkout', models.IntegerField()),
                ('totalRate', models.IntegerField()),
                ('is_promo', models.BooleanField(default=False)),
                ('is_package', models.BooleanField(default=False)),
                ('discountPercent', models.FloatField(default=0)),
                ('hotelTax', models.FloatField(default=0)),
                ('serviceCharge', models.FloatField(default=0)),
                ('airportTransfer', models.FloatField(default=0)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverApp.HotelInfo')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverApp.Traveller')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OverApp.Package')),
                ('promo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OverApp.HotelAvailability')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OverApp.RoomInfo')),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'BookCache',
            },
        ),
    ]
