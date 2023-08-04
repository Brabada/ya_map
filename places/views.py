from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse, JsonResponse
from django.urls import reverse
from places.models import Place


def index(request):
    features = []
    for place in Place.objects.all():
        features.append(
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [place.longitude, place.latitude],
                },
                'properties': {
                    'title': place.title,
                    'placeId': place.id,
                    'detailsUrl': reverse(get_place_details_json, kwargs={'place_id': place.id}),
                },
            }
        )
    places = {
        'places': {
            'type': 'FeatureCollection',
            'features': features,
        }
    }

    return render(request, 'index.html', context=places)


def get_place_details_json(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    place_detail = {
        'title': place.title,
        'imgs': [image.image.url for image in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude,
        },
    }

    return JsonResponse(data=place_detail, json_dumps_params={'ensure_ascii': False, 'indent': 4})

