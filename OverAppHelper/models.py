from __future__ import unicode_literals

from django.db import models

from OverApp.models import *

# Create your models here.

class BookCache(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    start = models.IntegerField()
    end = models.IntegerField()
    days = models.IntegerField()
    checkin = models.CharField(max_length=256, blank=True, null=True)
    checkout = models.CharField(max_length=256, blank=True, null=True)
    totalRate = models.IntegerField()
    is_promo = models.BooleanField(default=False)
    is_package = models.BooleanField(default=False)
    discountPercent = models.FloatField(default=0)
    hotelTax = models.FloatField(default=0)
    serviceCharge = models.FloatField(default=0)
    airportTransfer = models.FloatField(default=0)
    hotel = models.ForeignKey('OverApp.HotelInfo')
    traveller = models.ForeignKey('OverApp.Traveller')
    room = models.ForeignKey('OverApp.RoomInfo', blank=True, null=True)
    promo = models.ForeignKey('OverApp.HotelAvailability', blank=True, null=True)
    package = models.ForeignKey('OverApp.Package', blank=True, null=True)

    class Meta:
        managed=True
        verbose_name_plural = 'BookCache'

class BookingInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    cache = models.ForeignKey('OverAppHelper.BookCache')
    booking_id = models.CharField(max_length=5120)
    traveller = models.ForeignKey('OverApp.Traveller')

    class Meta:
        managed = True
        verbose_name_plural = 'BookingInfo'
