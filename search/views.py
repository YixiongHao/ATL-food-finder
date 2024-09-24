# Create your views here.
from django.shortcuts import render
import requests
from ATL_food_finder.settings import GOOGLE_API_KEY
from django.conf import settings
from django.http import JsonResponse
import rich

api_key = GOOGLE_API_KEY

'''def search_places(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}'

        response = requests.get(url)
        results = response.json().get('results', [])

        return render(request, 'search/search_results.html', {'results': results})
'''

def search_nearby_restaurants(request):
    geolocation_url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"

    try:
        response = requests.post(geolocation_url)
        location_data = response.json()
        print(location_data)

        if 'location' in location_data:
            lat = location_data['location']['lat']
            long = location_data['location']['lng']
            #accuracy = location_data['accuracy']

            radius = 1500  # placeholder, meters
            min_rating = 3 # placeholder

            # Use Google Places API to search for nearby restaurants
            query = request.GET.get('query', '')

            #url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&radius={radius}&type=restaurant&keyword={query}&key={api_key}'
            #response = requests.get(url)

            url = 'https://places.googleapis.com/v1/places:searchText'
            headers = {
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': api_key,
                'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,'
                                    + 'places.rating,places.userRatingCount,places.primaryType,places.editorialSummary,'
                                    + 'places.photos,places.currentOpeningHours,places.websiteUri,'
                                    + 'places.servesVegetarianFood,places.delivery,places.location,'
                                    + 'places.dineIn,places.takeout,places.reservable,places.outdoorSeating,'
                                    + 'places.goodForChildren,places.goodForGroups'

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

            #rich.print(filtered_results)
            context = {'results': filtered_results, 'google_maps_api_key': api_key}
            return render(request, 'search/search_results.html', context)
        else:
            return JsonResponse({'error': 'Location not found'}, status=400)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)