from django.shortcuts import render
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
