# REQUIREMENTS
import os
import json
import time
import requests
import json

# DJANGO
from django.core.management.base import BaseCommand, CommandError
from OverApp.models import HotelInfo

key = {
    'account_id': 'apmq0617g42w',
    'secret_key': 'spxvkj13nvz15y100qg30o'
}

{
    "input":["New York, NYC, Nueva York"],
    "key":"New York,US",
    "meta": {
        "latitude": 40.7127,
        "longitude": 74.0059
    },
    "score": 30
}

def send(entry):
    url = 'http://suggest.autocompleteapi.com/'+ key['account_id'] +'/global'
    data_json = json.dumps(entry)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': key['secret_key']
    }
    result = requests.put(url, data=data_json, headers=headers)
    print result


def main():
    hotels = HotelInfo.objects.all()

    for hotel in hotels:
        # feed destinations
        if hotel.destination:
            tokens = hotel.destination.split(' ')
            for token in tokens:
                entry = {
                    'input': token,
                    'key': token,
                    'score': 50
                }
                send(entry)

        if hotel.area:
            tokens = hotel.area.split(' ')
            for token in tokens:
                entry = {
                    'input': token,
                    'key': token,
                    'score': 20
                }
                send(entry)

        if hotel.hotelName:
            tokens = hotel.hotelName.split(' ')
            for token in tokens:
                entry = {
                    'input': token,
                    'key': hotel.hotelName,
                    'score': 60
                }
                send(entry)

        if hotel.hotelAddress:
            tokens = hotel.hotelAddress.split(' ')
            for token in tokens:
                entry = {
                    'input': token,
                    'key': token,
                    'score': 20
                }
                send(entry)

        if hotel.hotelAmens:
            tokens = hotel.hotelAmens.split(',')
            for token in tokens:
                entry = {
                    'input': token.rstrip(),
                    'key': token.rstrip(),
                    'score': 45
                }
                send(entry)

        if hotel.hotelServices:
            tokens = hotel.hotelServices.split(',')
            for token in tokens:
                entry = {
                    'input': token.rstrip(),
                    'key': token.rstrip(),
                    'score': 40
                }
                send(entry)

        if hotel.hotelRoomTypes:
            tokens = hotel.hotelRoomTypes.split(',')
            for token in tokens:
                entry = {
                    'input': token.rstrip(),
                    'key': token.rstrip(),
                    'score': 55
                }
                send(entry)


class Command(BaseCommand):

    help = 'A Worker Management Command Implementation'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            # Call Main
            main()
            self.stdout.write('Successfully updated')

        except Exception as e:
            print e