from django.core.exceptions import MultipleObjectsReturned
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
import requests

import json
import logging

from places.models import Place, Image


def parse_json(file_location):

    if file_location[:4] == 'http':
        response = requests.get(file_location)
        response.raise_for_status()
        place = response.json()
    else:
        with open(file_location, 'r', encoding='utf-8') as json_file:
            place = json.load(json_file)
    return place


def download_images(image_urls):

    image_binaries = []
    for image_url in image_urls:
        response = requests.get(image_url)
        response.raise_for_status()
        image_binaries.append(response.content)
    return image_binaries


def create_place(self, place):

    defaults = {
        'description_short': place['description_short'],
        'description_long': place['description_long'],
        'longitude': place['coordinates']['lng'],
        'latitude': place['coordinates']['lat'],
    }

    place, created = Place.objects.get_or_create(
        title=place['title'],
        defaults=defaults
    )

    logging.debug(f'Created is {created}')
    if not created:
        return

    binary_images = download_images(place['imgs'])
    for count, image in enumerate(binary_images):
        file = ContentFile(image, name=str(count))
        logging.debug(file)
        Image.objects.create(
            order=count,
            place=place,
            image=file)
    self.stdout.write(f'{place["title"]} was added to DB.')


class Command(BaseCommand):
    help = 'Parse title, coords, descriptions, image links from json and add as new Place object'

    def add_arguments(self, parser):

        parser.add_argument(
            'path_to_json',
            nargs='+',
            type=str,
            help='Relative, absolute path or link to place.json with filename. Ex: "./places_json/Воробьёвы горы.json",'
                 '" places_json\Водопад Радужный.json" "'
                 'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/place.json"'
        )

    def handle(self, *args, **options):

        for path_place in options['path_to_json']:
            try:
                place = parse_json(path_place)
                create_place(self, place)
            except MultipleObjectsReturned:
                message = f'There is multiple objects with {place["title"]} name with coords [{place["coordinates"]["lng"]},' \
                          f'{place["coordinates"]["lat"]}]'
                self.stderr.write(message)
            except requests.exceptions.HTTPError:
                self.stderr.write('Image not found.')

        self.stdout.write("Work's done")
