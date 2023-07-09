from django.core.exceptions import MultipleObjectsReturned
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
import requests

import json
import logging

from places.models import Place, Image


def parse_json(self, path_to_file):

    if path_to_file[:4] == "http":
        response = requests.get(path_to_file)
        response.raise_for_status()
        place_data = response.json()
    else:
        with open(path_to_file, 'r', encoding='utf-8') as json_file:
            place_data = json.load(json_file)
    return place_data


def download_images(image_urls):
    images_binary = []
    for image_url in image_urls:
        response = requests.get(image_url)
        response.raise_for_status()
        images_binary.append(response.content)
    return images_binary


def create_place(self, place):
    defaults = {
        'description_short': place['description_short'],
        'description_long': place['description_long'],
        'longitude': place['coordinates']['lng'],
        'latitude': place['coordinates']['lat'],
    }

    created_place, created = Place.objects.get_or_create(
        title=place['title'],
        defaults=defaults
    )
    logging.debug(f'Created is {created}')
    if not created:
        return

    binary_images = download_images(place['imgs'])
    for cnt, image in enumerate(binary_images):
        file = ContentFile(image, name=str(cnt))
        logging.debug(file)
        Image.objects.create(
            order=cnt,
            place=created_place,
            image=file)
    self.stdout.write(f"{place['title']} was added to DB.")


class Command(BaseCommand):
    help = "Parse title, coords, descriptions, image links from json and add as new Place object"

    def add_arguments(self, parser):
        parser.add_argument(
            "path_to_json",
            nargs='+',
            type=str,
            help='Relative, absolute path or link to place.json with filename. Ex: "./places_json/Воробьёвы горы.json", '
                 '"places_json\Водопад Радужный.json" "'
                 'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/place.json"'
        )

    def handle(self, *args, **options):

        for path_place in options["path_to_json"]:
            try:
                place = parse_json(self, path_place)
                create_place(self, place)
            except MultipleObjectsReturned:
                message = f'There is multiple objects with {place["title"]} name with coords [{place["coordinates"]["lng"]},' \
                          f'{place["coordinates"]["lat"]}]'
                self.stderr.write(message)
            except requests.exceptions.HTTPError:
                self.stderr.write('Image not found.')

        self.stdout.write("Work's done")
