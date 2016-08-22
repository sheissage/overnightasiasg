# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-11 13:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelInfo',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('hotelId', models.TextField(primary_key=True, serialize=False)),
                ('destination', models.CharField(blank=True, max_length=5120, null=True)),
                ('area', models.CharField(blank=True, max_length=5120, null=True)),
                ('hotelName', models.CharField(blank=True, max_length=5120, null=True)),
                ('hotelAddress', models.CharField(blank=True, max_length=5120, null=True)),
                ('hotelAmens', models.CharField(blank=True, max_length=5120, null=True)),
                ('hotelServices', models.CharField(blank=True, max_length=5120, null=True)),
                ('hotelRoomTypes', models.CharField(blank=True, max_length=5120, null=True)),
                ('priceByDate', models.CharField(blank=True, max_length=5120, null=True)),
                ('hotelPictures', models.ImageField(default='hotelPics/avatar.jpg', upload_to='hotelPics/')),
                ('hotelDescription', models.CharField(blank=True, max_length=5120, null=True)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'HotelInfo',
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('merchantId', models.AutoField(primary_key=True, serialize=False)),
                ('merchantName', models.CharField(max_length=5120)),
                ('email', models.CharField(max_length=5120)),
                ('phone', models.CharField(blank=True, max_length=5120, null=True)),
                ('streetAddr', models.CharField(blank=True, max_length=5120, null=True)),
                ('unit', models.CharField(blank=True, max_length=5120, null=True)),
                ('city', models.CharField(blank=True, max_length=5120, null=True)),
                ('state', models.CharField(blank=True, max_length=5120, null=True)),
                ('zip', models.CharField(blank=True, max_length=5120, null=True)),
                ('country', models.CharField(blank=True, max_length=5120, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Merchant',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('packageId', models.AutoField(primary_key=True, serialize=False)),
                ('packageName', models.CharField(blank=True, max_length=5120, null=True)),
                ('packageDesc', models.CharField(blank=True, max_length=5120, null=True)),
                ('price', models.FloatField(db_column='price', default=0)),
                ('currency', models.CharField(blank=True, max_length=5, null=True)),
                ('roomType', models.CharField(blank=True, max_length=5120, null=True)),
                ('serviceList', models.CharField(blank=True, max_length=5120, null=True)),
                ('discountPercent', models.FloatField(default=0)),
                ('hotelTax', models.FloatField(default=0)),
                ('serviceCharge', models.FloatField(default=0)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverApp.HotelInfo')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverApp.Merchant')),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Package',
            },
        ),
        migrations.CreateModel(
            name='RoomInfo',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('roomId', models.AutoField(primary_key=True, serialize=False)),
                ('roomType', models.CharField(blank=True, max_length=5120, null=True)),
                ('destination', models.CharField(blank=True, max_length=5120, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('ratePerNight', models.FloatField(default=0)),
                ('airportTransfer', models.FloatField(default=0)),
                ('discountPercent', models.FloatField(default=0)),
                ('hotelTax', models.FloatField(default=0)),
                ('serviceCharge', models.FloatField(default=0)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverApp.HotelInfo')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverApp.Merchant')),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'RoomInfo',
            },
        ),
        migrations.CreateModel(
            name='Traveller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(blank=True, max_length=5120, null=True)),
                ('fname', models.CharField(blank=True, max_length=5120, null=True)),
                ('lname', models.CharField(blank=True, max_length=5120, null=True)),
                ('email', models.CharField(blank=True, max_length=5120, null=True)),
                ('phone', models.CharField(blank=True, max_length=5120, null=True)),
                ('homeAirport', models.CharField(blank=True, max_length=5120, null=True)),
                ('streetAddr', models.CharField(blank=True, max_length=5120, null=True)),
                ('unit', models.CharField(blank=True, max_length=5120, null=True)),
                ('city', models.CharField(blank=True, max_length=5120, null=True)),
                ('state', models.CharField(blank=True, max_length=5120, null=True)),
                ('zip', models.CharField(blank=True, max_length=5120, null=True)),
                ('country', models.CharField(blank=True, max_length=5120, null=True)),
                ('gender', models.CharField(default='male', max_length=64)),
                ('travellerPictures', models.ImageField(default='img/300x300.png', upload_to='travellerPics/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Traveller',
            },
        ),
        migrations.AddField(
            model_name='package',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverApp.RoomInfo'),
        ),
        migrations.AddField(
            model_name='hotelinfo',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverApp.Merchant'),
        ),
    ]