from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse, JsonResponse
from places.models import Place
# Create your views here.


def index(request):

    features = []
    for place in Place.objects.all():
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.longitude, place.latitude],
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.id,
                    "detailsUrl": "",
                },
            }
        )
    places_json = {
        "type": "FeatureCollection",
        "features": features,
    }

    data = {
        'places': places_json,
    }

    return render(request, 'index.html', context=data)


def place_details(request, place_id):
    # place = get_object_or_404(Place, pk=place_id)
    # response = place.title
    # return HttpResponse(response)
    place = get_object_or_404(Place, id=place_id)
    place_json = {
        "title": place.title,
        "imgs": [image.image.url for image in place.images.all()],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.longitude,
            "lat": place.latitude,
        },
    }

    return JsonResponse(data=place_json, json_dumps_params={'ensure_ascii': False, 'indent': 4})
