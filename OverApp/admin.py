from django.contrib import admin
from .models import Merchant, HotelInfo, RoomInfo, Package, HotelAvailability, Traveller, Gallery
# Register your models here.


class MerchantAdmin(admin.ModelAdmin):
    list_display = ('merchantName', 'email')

class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotelName', 'destination')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('roomType', 'ratePerNight')

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room')


admin.site.register(Merchant, MerchantAdmin)
admin.site.register(HotelInfo, HotelAdmin)
admin.site.register(RoomInfo, RoomAdmin)
admin.site.register(Gallery, GalleryAdmin)