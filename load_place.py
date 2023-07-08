from django.core.exceptions import MultipleObjectsReturned
from django.core.files.base import ContentFile

from places.models import Place, Image

import json
import logging

import requests


def parse_json(path_to_file):

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


def create_place(place):

    # if not rounding coords before, get_or_create incorrectly comparing existing coords in DB cause DecimalField adding
    # zeroes if decimal places < 7. Ex: raw 1.234 -> 1.2340000
    # coords =
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
        file = ContentFile(image, name='')
        logging.debug(file)
        Image.objects.create(
            order=cnt,
            place=created_place,
            image=file)


def main():

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    place = parse_json('./places_json/Воробьёвы горы.json')
    logging.debug(json.dumps(place, indent=2))
    try:
        create_place(place)
    except MultipleObjectsReturned:
        message = f'There is multiple objects with {place["title"]} name with coords [{place["coordinates"]["lng"]},'\
            f'{place["coordinates"]["lat"]}]'
        logging.warning(message)
    except requests.exceptions.HTTPError:
        logging.warning(f'Image not found.')


if __name__ == "__main__":
    main()
