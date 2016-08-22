from __future__ import unicode_literals
from __future__ import division

import django
import json
import time
import stripe
import uuid

from searchModule import queryBuilder as qb

from .models import HotelInfo, RoomInfo, Merchant, Package, HotelAvailability, Traveller, Gallery
import models
from .utils import generic_search
from OverApp.helper import Helper
from OverAppHelper.models import BookCache, BookingInfo

###################
""" Dajngo libs"""
###################
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Q
from django.db import transaction
from django.conf import settings

from django.template import Context
from django.template.loader import get_template

from weasyprint import HTML, CSS


# Create your views here.

stripe_keys = {
    'secret_key': 'sk_live_caKZdIl4atGNWxyBvZqGbE9U',
    'publishable_key': 'pk_live_ncLqTFSAfTuKhOpVRPNNRgLi'
}

# stripe_keys = {
#     'secret_key': 'sk_test_vgwekv4idaRHxKy08tdqYcd4',
#     'publishable_key': 'pk_test_NqL1tDPNyP990ViPnvUfq8XY'
# }

def landing_page(request):
    return render(request, 'landingpage.html')


def loginTraveller(request):
    return render(request, 'login.html')


def travellerSignup(request):
    return render(request, 'signup.html')


def merchantSignup(request):
    return render(request, 'merchantSignup.html')


def loadMerchantLogin(request):
    return render(request, 'merchantLogin.html')


def loadDash(request):
    roomData = models.RoomInfo.objects.all().values()
    print("before max")
    getMax()
    print("After max")
    print(roomData)
    return render(request, 'hotelDashboard.html', {'roomdata': roomData})


def getContent(request):
    print("here")
    res = ''
    if request.method == 'POST':
        params = request.POST
        val = params.get('search_keyword')
        print(val)

        print("outside")
    # return HttpResponse(json.dumps({'data': res}),
    # content_type="application/json")
    return render(request, 'landingpage.html', {'data': res})


def showSearchResult(request):
    return render(request, 'searchresults_common.html')


def uploadPage(request):
    return render(request, 'uploadPics.html')


def manageContent(request):
    user = request.user
    merchant = Merchant.objects.get(user=user)
    hotels = HotelInfo.objects.filter(merchant=merchant).values('hotelId', 'hotelName')
    context = {
        'hotels': hotels
    }
    return render(request, 'manageContent.html', context)


def showBookingConfirmation(request):
    return render(request, 'bookingconfirmation.html')

@login_required
def showUserProfile(request):
    traveller  = Traveller.objects.get(user=request.user)
    name = traveller.fname + ' ' + traveller.lname

    bookings = BookingInfo.objects.filter(traveller=traveller).values_list('cache')
    booking_info = BookCache.objects.filter(pk__in=bookings)

    hotel_list = booking_info.values_list('hotel')
    hotels = HotelInfo.objects.filter(pk__in=hotel_list)
    cities = booking_info.distinct('hotel').count()
    trips = booking_info.count()
    address = ''
    if traveller.streetAddr:
        address = traveller.streetAddr + ' '
    if traveller.city:
        address = traveller.city + ' '
    if traveller.state:
        address = traveller.state + ' '
    if traveller.country:
        address = traveller.country + ' '

    context = {
        'name': name,
        'cities': cities,
        'trips': trips,
        'address': address
    }
    return render(request, 'user-profile.html', context)

@login_required
def showUserProfileBookingHistory(request):
    traveller  = Traveller.objects.get(user=request.user)
    name = traveller.fname + ' ' + traveller.lname

    bookings = BookingInfo.objects.filter(traveller=traveller).order_by('-created')[:10]
    # booking_info = BookCache.objects.filter(pk__in=bookings)

    context = {
        'name': name,
        'bookings': bookings
    }
    return render(request, 'user-profile-booking-history.html', context)

@login_required
def showUserProfileCards(request):
    if request.method == 'GET':
        traveller = Traveller.objects.get(user=request.user)
        galleries = Gallery.objects.filter(traveller=traveller)
        context = {
            'galleries': galleries
        }

    return render(request, 'user-profile-photos.html', context)


def showUserProfileSettings(request):
    if request.method == 'GET':
        traveller  = Traveller.objects.get(user=request.user)
        name = traveller.fname + ' ' + traveller.lname
        context = {
            'name': name,
            'traveller': traveller
        }
        return render(request, "user-profile-settings.html", context)
    elif request.method == 'POST':
        
        traveller  = Traveller.objects.get(user=request.user)
        params = request.POST
        try:
            traveller.fname = params.get('fname')
            traveller.lname = params.get('lname')
            traveller.email = params.get('email')
            traveller.phone = params.get('phone')
            traveller.streetAddr = params.get('streetAddr')
            traveller.city = params.get('city')
            traveller.state = params.get('state')
            traveller.zip = params.get('zip')
            traveller.country = params.get('country')

            traveller.save()
            context = {
                'user_status': 'Profile Saved',
                'traveller': traveller
            }
        except:
            context = {
                'user_status': 'Something went wrong!',
                'traveller': traveller
            }
        

        return render(request, "user-profile-settings.html", context)


def changepasswd(request):
    if request.method == 'POST':
        params = request.POST
        current_password = params.get('current_password')
        new_password = params.get('new_password')
        new_password_again = params.get('new_password_again')

        user = authenticate(username=request.user.email, password=current_password)
        traveller = Traveller.objects.get(user=user)
        if user is not None:
            if new_password != new_password_again:
                context = {
                    'pass_status': 'New Passwords do not match',
                    'traveller': traveller
                }
                return render(request, "user-profile-settings.html", context)
            else:
                user.set_password(new_password)
                user.save()
                context = {
                    'pass_status': 'Saved!',
                    'traveller': traveller
                }
                return render(request, "user-profile-settings.html", context)

        else:
            context = {
                    'pass_status': 'Wrong current password.',
                    'traveller': traveller
                }
            return render(request, "user-profile-settings.html", context)

        


@login_required
def addAvailability(request):
    if request.method == 'POST':
        params = request.POST
        room_pk = int(params.get("roomType"))
        hotel_pk = params.get('hotel')

        start = params.get("start")
        end = params.get("end")

        serviceCharge = params.get('servicecharge')
        
        price = params.get("price")
        discount = params.get('discount')
        hotelTax = params.get('hoteltax')

        price_type = params.get('roomPriceType')

        available = params.get('available')
            

        pattern = '%Y-%m-%d'
        start_epoch = int(time.mktime(time.strptime(start, pattern)))
        end_epoch = int(time.mktime(time.strptime(end, pattern)))

        merchant = Merchant.objects.get(user=request.user)
        hotel = HotelInfo.objects.get(merchant=merchant, pk=hotel_pk)
        room = RoomInfo.objects.get(hotel=hotel, pk=room_pk)
        
        if available == 'false':
            availabilities = HotelAvailability.objects.filter(
                merchant=merchant,
                hotel=hotel,
                room=room)\
                .filter(Q(start__range=(start_epoch, end_epoch)) | Q(end__range=(start_epoch, end_epoch)))
            if availabilities:
                availabilities.delete()

            availability = HotelAvailability(
                start=start_epoch, 
                end=end_epoch,
                is_available=False,
                merchant=merchant,
                hotel=hotel,
                room=room
            )
            return redirect('hotel-dashboard')
        if price_type == 'default':
            try:
                room.ratePerNight = float(price)
                room.discountPercent = float(discount)
                room.hotelTax = float(hotelTax)
                room.serviceCharge = float(serviceCharge)
                room.save()
            except:
                return HttpResponse('Pleas input 0 instead of blanks or be sure to populate all the field in Numeric form. Thanks!')

            return redirect('hotel-dashboard')

        #####################################################
        """ check if date availability is already present """
        #####################################################
        availabilities = HotelAvailability.objects.filter(
            merchant=merchant,
            hotel=hotel,
            room=room
        )

        for availability in availabilities:
            date_range = range(availability.start, availability.end)
            if start_epoch in date_range or end_epoch in date_range:
                return HttpResponse('Invalid - Overlapping Seasonal Rates')


        availability = HotelAvailability(
            start=start_epoch, 
            end=end_epoch,
            discountPercent=float(discount),
            hotelTax=float(hotelTax),
            serviceCharge=float(serviceCharge),
            ratePerNight=float(price),
            merchant=merchant,
            hotel=hotel,
            room=room
        )
        availability.save()

    return redirect('hotel-dashboard')

@login_required
def managePackage(request):
    merchant = Merchant.objects.get(user=request.user)
    hotels = HotelInfo.objects.filter(merchant=merchant).values('hotelId', 'hotelName')
    packages = Package.objects.filter(merchant=merchant)

    context = {
        'hotels': hotels,
        'packages': packages
    }
    return render(request, "managePackage.html", context)

@login_required
def createPackage(request):
    if request.method == 'POST':
        name = request.POST['name']
        packagedesc = request.POST['packagedesc']
        price = request.POST['price']
        services = request.POST['services']
        room_pk = int(request.POST['roomType'])
        hotel = request.POST['hotel']
        servicecharge = request.POST['servicecharge']
        hoteltax = request.POST['hoteltax']

        merchant = Merchant.objects.get(user=request.user)
        hotel = HotelInfo.objects.get(merchant=merchant, pk=hotel)

        room = RoomInfo.objects.get(merchant=merchant, hotel=hotel, pk=room_pk)

        package = models.Package(
            packageName=name, 
            packageDesc=packagedesc,
            price=float(price),
            roomType=room.roomType, 
            serviceList=services,
            hotelTax=hoteltax,
            serviceCharge=servicecharge,
            merchant=merchant,
            hotel=hotel,
            room=room
            )
        package.save()
        
        return redirect('hotel-dashboard')

@login_required
def updatePackage(request):
    if request.method == 'POST':

        packageId = request.POST['packageId']
        name = request.POST['name']
        packagedesc = request.POST['packagedesc']
        price = request.POST['price']
        services = request.POST['services']
        room_pk = int(request.POST['roomType'])
        hotel = request.POST['hotel']
        servicecharge = request.POST['servicecharge']
        hoteltax = request.POST['hoteltax']

        merchant = Merchant.objects.get(user=request.user)
        hotel = HotelInfo.objects.get(merchant=merchant, pk=hotel)

        room = RoomInfo.objects.get(merchant=merchant, hotel=hotel, pk=room_pk)

        package = Package.objects.get(pk=packageId, merchant=merchant)
        
        package.packageName = name
        package.packageDesc = packagedesc
        package.price = float(price)
        package.roomType = room.roomType
        package.serviceList = services
        package.hotelTax = hoteltax
        package.serviceCharge = servicecharge
        package.merchant = merchant
        package.hotel = hotel
        package.room = room
            
        package.save()
        
        return redirect('manage-package')

@login_required
def deletePackage(request):
    if request.method == 'GET':
        try:
            merchant = Merchant.objects.get(user=request.user)
            packageId = request.GET.get('packageId','')
            Package.objects.get(pk=packageId, merchant=merchant).delete()
            return JsonResponse({
                    'status': 200
                })
        except:
            return JsonResponse({
                    'status': 400
                })
        
@login_required
def updateHotel(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        hotelId = request.POST['hotelId']
        destination = request.POST['destination']
        name = request.POST['name']
        description = request.POST['description']
        address = request.POST['address']
        amenities = request.POST['amenities']
        services = request.POST['services']
        roomtypes = request.POST['roomtype']
        currency = request.POST['currency']
        airporttransfer = request.POST['airporttransfer']
        room_types = roomtypes.split(',')

        merchant = Merchant.objects.get(user=request.user)
        
        ##################
        """ save hotel """
        ##################
        hotel = HotelInfo.objects.get(pk=hotelId,merchant=merchant)
        hotel.hotelName = name
        hotel.hotelDescription = description
        hotel.destination = destination
        hotel.hotelAddress = address
        hotel.hotelAmens = amenities
        hotel.hotelServices = services
        hotel.hotelRoomTypes = roomtypes
        hotel.currency = currency
        hotel.airportTransfer = float(airporttransfer)

        hotel.save()

        ##################
        """ save rooms """
        ##################
        RoomInfo.objects.filter(hotel=hotel,merchant=merchant).delete()
        for room_type in room_types:
            room = RoomInfo(
                hotel=hotel, 
                merchant=merchant, 
                roomType=room_type.upper().strip(), 
                destination=destination,
                ratePerNight=0,
                discountPercent=0, airportTransfer=0,
                serviceCharge=0, hotelTax=0
            )

            room.save()

        ##################
        """ delete galleries """
        ##################

        Gallery.objects.filter(hotel=hotel).delete()

        request.session['sess_hotelId'] = hotelId

    return render(request, 'uploadPics.html', {"data": hotelId})

@login_required
def createHotel(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        destination = request.POST['destination']
        name = request.POST['name']
        description = request.POST['description']
        address = request.POST['address']
        amenities = request.POST['amenities']
        services = request.POST['services']
        roomtypes = request.POST['roomtype']
        currency = request.POST['currency']
        airporttransfer = request.POST['airporttransfer']

        maxindex = int(getMax()) + 1
        
        hotelId = destination + '-' + str(maxindex)
        room_types = roomtypes.split(',')

        merchant = Merchant.objects.get(user=request.user)
        
        ##################
        """ save hotel """
        ##################

        hotel = HotelInfo(
            hotelName=name,
            hotelDescription=description,
            hotelId=hotelId, 
            destination=destination,
            hotelAddress=address, 
            hotelAmens=amenities,
            hotelServices=services,
            hotelRoomTypes=roomtypes,
            merchant=merchant,
            currency=currency,
            airportTransfer=float(airporttransfer)
        )

        hotel.save()

        ##################
        """ save rooms """
        ##################
        
        for room_type in room_types:
            room = RoomInfo(
                hotel=hotel, 
                merchant=merchant, 
                roomType=room_type.upper().strip(), 
                destination=destination,
                ratePerNight=0,
                discountPercent=0, airportTransfer=0,
                serviceCharge=0, hotelTax=0
            )

            room.save()

        request.session['sess_hotelId'] = hotelId

    return render(request, 'uploadPics.html', {"data": hotelId})

@login_required
def deleteHotel(request):
    if request.method == 'GET':
        try:
            merchant = Merchant.objects.get(user=request.user)
            hotelId = request.GET.get('hotelId','')
            HotelInfo.objects.get(pk=hotelId, merchant=merchant).delete()
            return JsonResponse({
                    'status': 200
                })
        except:
            return JsonResponse({
                    'status': 400
                })

@login_required
def upload_user_pics(request):
    if request.method == 'POST':
        traveller = Traveller.objects.get(user=request.user)
        print 'yow'
        try:
            galleries = request.FILES.pop('galleries')
            for gallery in galleries:
                print gallery
                picture = Gallery(
                    picture=gallery,
                    traveller=traveller
                )
                picture.save()
            return redirect('user-photos')
        except:
            context = {
                'error': 'Please upload at least 1 Gallery Picture'
            }
            return render(request, 'user-profile-photos.html', context)
            
@login_required
def uploadPics(request):
    hotelId = request.session['sess_hotelId']
    hotel = HotelInfo.objects.get(hotelId=hotelId)
    hotel.hotelPictures = request.FILES.get('hotelImage', '')
    hotel.save()

    try:
        galleries = request.FILES.pop('galleries')
        for gallery in galleries:
            picture = Gallery(
                picture=gallery,
                hotel=hotel
            )
            picture.save()

        return redirect('hotel-dashboard')
    except:
        context = {
            'data': hotelId,
            'error': 'Please upload at least 1 Gallery Picture'
        }
        return render(request, 'uploadPics.html', context)


def createMerchant(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        try:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            repass = request.POST['repass']
        

            if repass == password:
                user = User.objects.create_user(
                    username=email, email=email, password=password)
                user.first_name = fname
                user.last_name = lname
                user.save()

                merchant = Merchant(
                    user=user,
                    merchantName=user.first_name + ' ' + user.last_name,
                    email=user.email
                )
                merchant.save()

                if user is None:
                    return render(request, "merchantSignup.html", {'error': "Something went worng. Please try again."})
                subject = "Welcome to Overnight.asia"
                from_email = 'welcome@overnight.asia'
                to = email
                text_content = 'Thank you for signing up as a partner. ' + \
                    user.first_name+"\n You're one of the #Overnight20 partners."
                html_content = '<p>Thank you for signing up as a partner.</p>'
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return render(request, 'merchantLogin.html')
            else:
                return render(request, "merchantSignup.html", {'error': "Passwords do not match"})
        except:
            return render(request, "merchantSignup.html", {'error': "Please provide all infromation."})

def getRoomTypes(request):
    if request.method == 'GET' and request.is_ajax:
        hotelId = request.GET.get('hotelId', '')
        hotel = HotelInfo.objects.get(hotelId=hotelId)
        roomTypes = RoomInfo.objects.filter(hotel=hotel)
        result = []

        for roomType in roomTypes:
            cache = {}
            cache['pk'] = roomType.pk
            cache['roomType'] = roomType.roomType
            
            result.append(cache)
        return JsonResponse(result, safe=False)

def getPackageInfo(request):
    if request.method == 'GET' and request.is_ajax:

        merchant = Merchant.objects.get(user=request.user)
        packageId = request.GET.get('packageId', '')
        package = Package.objects.get(pk=packageId, merchant=merchant)
        
        cache = {}
        cache['id'] = package.packageId
        cache['hotel'] = package.hotel.pk
        cache['name'] = package.packageName
        cache['description'] = package.packageDesc
        cache['price'] = package.price
        cache['room'] = package.room.pk
        cache['servicelist'] = package.serviceList
        cache['discount'] = package.discountPercent
        cache['tax'] = package.hotelTax
        cache['servicecharge'] = package.serviceCharge

        return JsonResponse(cache, safe=False)

def getBookingOffers(request):
    if request.method == 'GET':
        hotelId = request.GET.get('hotelId', '')
        error = request.GET.get('error', '')
        start = int(time.mktime(time.gmtime()))
        print start

        try:
            merchant = Merchant.objects.get(user=request.user)
        except:
            pass
        hotel = HotelInfo.objects.get(hotelId=hotelId)

        response = {}

        packages = Package.objects.filter(hotel=hotel, is_deleted=False, is_active=True).values('packageName', 'pk')
        dates = HotelAvailability.objects.filter(hotel=hotel, end__gte=start).values('start', 'end', 'pk')
        rooms = RoomInfo.objects.filter(hotel=hotel).values('pk', 'roomType')

        for date in dates:
            date['str_start'] = time.strftime('%b %d %Y', time.localtime(date.get('start')))
            date['str_end'] = time.strftime('%b %d %Y', time.localtime(date.get('end')))

        galleries = Gallery.objects.filter(hotel=hotel)

        context = {
            'defaults': rooms,
            'packages': packages,
            'promos': dates,
            'hotel': hotel,
            'hotelId': hotelId,
            'galleries': galleries
        }
        if error:
            context['error'] = error
        return render(request, 'viewDetails.html', context)


def getBookingOfferDetails(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        hotelId = request.GET.get('hotelId', '')
        start = request.GET.get('start', '')
        end = request.GET.get('end', '')
        offer_type = request.GET.get('type', '')

        pattern = '%Y-%m-%d'
        start_epoch = int(time.mktime(time.strptime(start, pattern)))
        end_epoch = int(time.mktime(time.strptime(end, pattern)))

        days = int((end_epoch-start_epoch)/84600)


        hotel = HotelInfo.objects.get(hotelId=hotelId)

        if offer_type == 'package':
            package = Package.objects.get(pk=pk)

            total_price = package.price * days

            total_tax = total_price * float((package.hotelTax/100))
            total_servicecharge = total_price * float((package.serviceCharge/100))
            total = (total_price + total_tax) + total_servicecharge
            response = {
                'package_name': package.packageName,
                'package_description': package.packageDesc,
                'package_total': "{0:.2f}".format(total),
                'package_currency': hotel.currency
            }
        elif offer_type == 'promo':
            promo = HotelAvailability.objects.get(pk=pk)

            total_price = promo.ratePerNight * days

            total_discount = (total_price * float((promo.hotelTax/100)))
            total_tax = (total_price * float((promo.hotelTax/100)))
            total_servicecharge = (total_price * float((promo.serviceCharge/100)))
            total = (total_price - total_discount) + total_tax + total_servicecharge
            response = {
                'promo_name': 'Promo Price ({0} - {1})'.format(start, end),
                'promo_description': 'Enjoy the all in price of {0}'.format(total),
                'promo_total': "{0:.2f}".format(total),
                'promo_currency': hotel.currency
            }
        else:
            room = RoomInfo.objects.get(pk=pk)

            total_price = (room.ratePerNight * days)

            total_tax = (total_price * float((room.hotelTax/100)))
            total_servicecharge = (total_price * float((room.serviceCharge/100)))
            total = total_price + total_tax + total_servicecharge
            response = {
                'room_name': room.roomType,
                'room_description': 'Enjoy the usual and comfy experience of the {0} room at {1}'.format(room.roomType, total),
                'room_total': "{0:.2f}".format(total),
                'room_currency': hotel.currency
            }

        return JsonResponse(response)


@transaction.atomic
def getBookingDetails(request):
    if request.method == 'GET':

        ############################
        """ pbooking variables """
        ############################
        start_epoch = 0
        end_epoch = 0
        total = 0
        is_promo = False
        is_package = False
        tax = 0
        service_charge = 0
        room_type = None
        promo = None
        package = None
        airport_transfer = 0

        try:
            hotelId = request.GET.get('hotelId', '')
            start = request.GET.get('start', '')
            end = request.GET.get('end', '')
            pk = request.GET.get('pk', '')
            offer_type = request.GET.get('type', '')

            pattern = '%Y-%m-%d'
            start_epoch = int(time.mktime(time.strptime(start, pattern)))
            end_epoch = int(time.mktime(time.strptime(end, pattern)))
        except:
            response = redirect('hotel-booking-offers')
            response['Location'] += '?error=Please select a corresponding Room, Package or Promo to proceed&hotelId=' + hotelId
            return response

        days = int((end_epoch-start_epoch)/84600)
        hotel = HotelInfo.objects.get(hotelId=hotelId)
        airport_transfer = hotel.airportTransfer
        total_discount = 0
        room = None
        try:
            traveller = Traveller.objects.get(user=request.user)
        except:
            return render(request, 'login.html')

        if offer_type == 'package':
            is_package = True
            package = Package.objects.get(pk=pk)
            tax = package.price
            service_charge = package.serviceCharge

            total_price = (package.price * days)

            total_tax = (total_price * float((package.hotelTax/100)))
            total_servicecharge = (total_price * float((package.serviceCharge/100)))
            total = total_price + total_tax + total_servicecharge
            
        elif offer_type == 'promo':
            is_promo = True
            promo = HotelAvailability.objects.get(pk=pk)
            tax = promo.hotelTax
            service_charge = promo.serviceCharge
            room_type = promo.room.roomType
            total_price = promo.ratePerNight * days

            total_discount = (total_price * float((promo.hotelTax/100)))
            total_tax = (total_price * float((promo.hotelTax/100)))
            total_servicecharge = (total_price * float((promo.serviceCharge/100)))
            total = (total_price - total_discount) + total_tax + total_servicecharge
            
        else:
            room = RoomInfo.objects.get(pk=pk)
            tax = room.hotelTax
            service_charge = room.serviceCharge
            room_type = room.roomType
            total_price = (room.ratePerNight * days)

            total_tax = (total_price * float((room.hotelTax/100)))
            total_servicecharge = (total_price * float((room.serviceCharge/100)))
            total = total_price + total_tax + total_servicecharge

        
        request.price = "{0:.2f}".format(total)

        ############################
        """ create booking cache"""
        ############################

        cache = BookCache()

        cache.start = start_epoch
        cache.end = end_epoch
        cache.days = days

        cache.totalRate = float(total)
        cache.is_promo = is_promo
        cache.is_package = is_package
        cache.discountPercent = float(total_discount)
        cache.hotelTax = float(tax)
        cache.serviceCharge = float(service_charge)
        # airportTransfer = models.FloatField(default=0)
        cache.hotel = hotel
        cache.traveller = Traveller.objects.get(user=request.user)
        cache.room = room
        cache.promo = promo
        cache.package = package

        cache.save()

        context = {
            'total_price': total_price,
            'total_tax': total_tax,
            'total_servicecharge':total_servicecharge,
            'final_price': "{0:.2f}".format(total),
            'stripe_final_price': "{0:.2f}".format(total*100),
            'currency': hotel.currency,
            'hotel_name': hotel.hotelName,
            'hotel_address': hotel.hotelAddress,
            'airport_transfer': airport_transfer,
            'total_price_transfer': "{0:.2f}".format((total + airport_transfer)*100),
            'cache': cache.pk
        }
        if total_discount:
            context['total_discount'] = total_discount
        if room:
            context['room'] = room

        return render(request, 'bookingdetails.html', context)


def getHotelInfo(request):
    if request.method == 'GET' and request.is_ajax:
        merchant = Merchant.objects.get(user=request.user)
        
        hotelId = request.GET.get('hotelId', '')

        hotel = HotelInfo.objects.get(merchant=merchant, pk=hotelId)

        cache = {}
        cache['destination'] = hotel.destination
        cache['area'] = hotel.area
        cache['hotelName'] = hotel.hotelName
        cache['hotelAddress'] = hotel.hotelAddress
        cache['hotelAmens'] = hotel.hotelAmens
        cache['hotelServices'] = hotel.hotelServices
        cache['hotelRoomTypes'] = hotel.hotelRoomTypes
        cache['hotelDescription'] = hotel.hotelDescription
        cache['currency'] = hotel.currency
        cache['airporttransfer'] = hotel.airportTransfer

        return JsonResponse(cache, safe=False)


def getRoomInfo(request):
    if request.method == 'GET' and request.is_ajax:
        merchant = Merchant.objects.get(user=request.user)
        roomId = request.GET.get('roomId', '')

        room = RoomInfo.objects.get(merchant=merchant, pk=roomId)

        # result = []
        cache = {}
        cache['ratePerNight'] = room.ratePerNight
        cache['discountPercent'] = room.discountPercent
        cache['hotelTax'] = room.hotelTax
        cache['serviceCharge'] = room.serviceCharge
        # result.append(cache)
        return JsonResponse(cache, safe=False)

def getRoomAvailability(request):
    if request.method == 'GET' and request.is_ajax:
        merchant = Merchant.objects.get(user=request.user)
        roomId = request.GET.get('roomId', '')
        start =  request.GET.get('start', '')
        end =  request.GET.get('end', '')

        room = RoomInfo.objects.get(merchant=merchant, pk=roomId)

        dates = HotelAvailability.objects.filter(room=room)\
            .filter(Q(start__range=(start, end)) | Q(end__range=(start, end)))

        result = []
        for date in dates:
            cache = {}
            start = int(time.strftime('%d', time.localtime(date.start)))
            end = int(time.strftime('%d', time.localtime(date.end)))
            if start > end:
                end = 31

            cache['start'] = start
            cache['end'] = end
            cache['rate'] = date.ratePerNight
            result.append(cache)
        return JsonResponse(result, safe=False)

def logonMerchant(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)
                try:
                    merchant = Merchant.objects.get(user=user)
                except:
                    return render(request, 'merchantLogin.html', {'error':'Invalid User'})
                return redirect('hotel-dashboard')
            return render(request, 'merchantLogin.html', {'error':'User not active'})
        return render(request, 'merchantLogin.html', {'error':'Invalid User'})


def hotelDashboardRedirect(request):
    merchant = Merchant.objects.get(user=request.user)
    hotels = HotelInfo.objects.filter(merchant=merchant).values('hotelId', 'hotelName')
    context = {
        'hotels': hotels
    }
    return render(request, "hotelDashboard.html", context, content_type="text/html")


def getMax():
    hotel = HotelInfo.objects.all().order_by('-created').first()
    if not hotel:
        return 0
    max_id = (hotel.hotelId).split('-')[1]

    return max_id

def authenticateUser(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["passwd"]
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                traveller = Traveller.objects.filter(user=user)
                if traveller:
                    login(request, user)
                    resp = landing_page(request)
                    return resp
        
        return render(request, "login.html", {'error': 'Not a registered Traveller'}, content_type="text/html")

def signupFirsttoSecond(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        
        context = {
            'firstname': firstname,
            'lastname': lastname
        }
        return render(request, 'signup2.html',  context)

def createTaveller(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        
        if password == repassword:
            try:
                user = User.objects.create_user(
                    username=email, email=email, password=password)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
            except:
                return HttpResponse('User email already exists')

            traveller = Traveller(
                fname=firstname, 
                lname=lastname,
                email=email,
                gender=gender,
                user=user
            )
            traveller.save()

            subject = 'Welcome to Overnight.asia'
            from_email = 'welcome@overnight.asia'
            to = email
            text_content = "a beta member of Overnight.asia."
            html_content = '<p>Hello! ' + firstname + \
                '<br> Thank you for signing on '\
                '<strong>Overnight.asia</strong> .</p>'
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            context = {
                'user': traveller.pk
            }

            return render(request, 'signup3.html',  context)
        else:
            return HttpResponse('Passwords Do not match')

def createTravellerAddress(request):
    if request.method == 'POST':
        country = request.POST['country']
        city = request.POST['city']
        street = request.POST['street']
        unit = request.POST['unit']
        zipcode = request.POST['zip']

        pk = int(request.POST['user'])

        try:
            traveller = Traveller.objects.get(pk=pk)
            traveller.country = country
            traveller.city = city
            traveller.streetAddr = street
            traveller.unit = unit
            traveller.zip = zipcode

            traveller.save()

            return render(request, 'landingpage.html')
        except Exception as e:
            print e
            return HttpResponse('Something wrong')



def search(request):
    webquery = request.GET.get('searchbar')
    
    MODEL_MAP = {
        HotelInfo: ['destination', 'area', 'hotelName', 'hotelAddress', 'hotelAmens', 'hotelServices', 'hotelDescription', 'hotelRoomTypes',]
    }
    objects = []

    for model,fields in MODEL_MAP.iteritems():
        objects+=generic_search(request, model, fields, webquery)
        
    context = {
        'hotels': objects,
        'count': len(objects),
        'query': webquery
    }
    return render(request, 'searchresults_common.html', context)

def book(request):
    if request.method == 'POST':
        cache_pk = request.POST.get('cache')
        cache = BookCache.objects.get(pk=cache_pk)
        if not cache:
            traveller = Traveller.objects.get(user=request.user)
            try:
                cache = BookCache.objects.filter(traveller).order_by('-created').first()
            except:
                #return error
                pass

        cache.checkin = str(request.POST.get('checkin_hr')) + ':' + str(request.POST.get('checkin_min')) +  ' ' + request.POST.get('checkin_mer')
        cache.checkout = str(request.POST.get('checkout_hr')) + ':' + str(request.POST.get('checkout_min')) +  ' ' + request.POST.get('checkout_mer')
        
        is_transfer = request.POST.get('transfer')

        cache.save()
        stripe.api_key = stripe_keys['secret_key']

        customer = stripe.Customer.create(
            email=cache.traveller.email,
            source=request.POST.get('stripeToken')
        )
        amount = cache.totalRate
        if is_transfer == 'true':
            amount += cache.hotel.airportTransfer
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=int(amount),
            currency=cache.hotel.currency,
            description='Overnight Booking'
        )
        uid = uuid.uuid4()
        uid = str(uuid.uuid4())
        book_id = uid.split('-')[4]

        book = BookingInfo()
        book.booking_id = book_id.upper()
        book.cache = cache
        book.traveller = cache.traveller
        book.save()

        """ Create and send PDF"""          
        

        context = {
            'cache': cache,
            'book': book,
            'start': time.strftime('%b %d %Y', time.localtime(cache.start)),
            'end': time.strftime('%b %d %Y', time.localtime(cache.end)),
        }

        # 
        html_template = get_template('bookingconfirmation.html')
        user = request.user

        rendered_html = html_template.render(RequestContext(request, context)).encode(encoding="UTF-8")
        pdf_file = HTML(string=rendered_html).write_pdf()

        Helper.send_booking_email(cache.traveller.email, pdf_file)
        # http_response = HttpResponse(pdf_file, content_type='application/pdf')
        # http_response['Content-Disposition'] = 'filename="itenerary.pdf"'

        return render(request, 'bookingconfirmation.html', context)

def showeResults(request):
    pass

@login_required
def logout_user(request):
    logout(request)
    return render(request, "landingpage.html")