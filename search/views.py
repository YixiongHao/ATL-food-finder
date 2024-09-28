# Create your views here.
from django.shortcuts import render
import requests
from ATL_food_finder.settings import GOOGLE_API_KEY
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import rich
import json

def search_nearby_restaurants(request):
    api_key = GOOGLE_API_KEY
    geolocation_url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"

    try:
        response = requests.post(geolocation_url)
        location_data = response.json()

        if 'location' in location_data:
            lat = location_data['location']['lat']
            long = location_data['location']['lng']

            #get search params
            query = request.GET.get('query', '')
            radius = int(request.GET.get('radius', 50000))
            min_rating = int(request.GET.get('min_rating', 0))

            url = 'https://places.googleapis.com/v1/places:searchText'
            headers = {
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': api_key,
                'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,'
                                    + 'places.rating,places.types,places.primaryType,places.editorialSummary,'
                                    + 'places.photos,places.currentOpeningHours,places.websiteUri,'
                                    + 'places.servesVegetarianFood,places.delivery,places.location,'
                                    + 'places.dineIn,places.takeout,places.reservable,places.outdoorSeating,'
                                    + 'places.reviews'

            }
            data = {
                'textQuery': query,
                'locationBias': {
                    'circle': {
                        'center': {
                            'latitude': float(lat),
                            'longitude': float(long)
                        },
                        'radius': radius
                    }
                },
                'includedType' : 'restaurant'
            }

            response = requests.post(url, json=data, headers=headers)
            results = response.json().get('places', [])
            if not results:
                print("No results found")
                print(response.json())  # Print the full response for debugging

            filtered_results = [place for place in results if (place.get('rating', 0) >= min_rating)]

            context = {'results': filtered_results, 'google_maps_api_key': api_key}
            return render(request, 'search/search_results.html', context)
        else:
            return JsonResponse({'error': 'Location not found'}, status=400)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)