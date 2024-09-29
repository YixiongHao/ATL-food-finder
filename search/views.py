# Create your views here.
from django.shortcuts import render
import requests
from ATL_food_finder.settings import GOOGLE_API_KEY
from django.conf import settings
from django.http import JsonResponse
from math import radians, sin, cos, sqrt, atan2


def search_nearby_restaurants(request):
    api_key = GOOGLE_API_KEY
    geolocation_url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"

    try:
        # Requesting geolocation from Google API
        response = requests.post(geolocation_url)
        location_data = response.json()

        if 'location' in location_data:
            lat = location_data['location']['lat']
            long = location_data['location']['lng']

            # Get search parameters from the request
            query = request.GET.get('query', '')
            radius = int(request.GET.get('radius', 50000))  # Default radius is 50000 meters
            min_rating = int(request.GET.get('min_rating', 0))  # Default minimum rating is 0

            # Construct the request to Google Places API
            url = 'https://places.googleapis.com/v1/places:searchText'
            headers = {
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': api_key,
                'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.priceLevel,'
                                    'places.rating,places.types,places.primaryType,places.editorialSummary,'
                                    'places.photos,places.currentOpeningHours,places.websiteUri,'
                                    'places.servesVegetarianFood,places.delivery,places.location,'
                                    'places.dineIn,places.takeout,places.reservable,places.outdoorSeating,'
                                    'places.reviews'
            }
            data = {
                "rankPreference": "DISTANCE",
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
                'includedType': 'restaurant'
            }

            # Send POST request to the Google Places API
            response = requests.post(url, json=data, headers=headers)
            results = response.json().get('places', [])

            # Handle case where no results are found
            if not results:
                print("No results found")
                print(response.json())  # Print the full response for debugging

            # Calculate the distance for each place and parse the cuisine type
            for place in results:
                place['distance'] = calculate_distance(lat, long, place['location']['latitude'],
                                                       place['location']['longitude'])
                place['cuisine'] = parse_underscore(place['primaryType'])

            # Filter results based on minimum rating
            filtered_results = [place for place in results if place.get('rating', 0) >= min_rating]

            # Prepare context to pass to the template
            context = {
                'results': [
                    {
                        'id': place['id'],
                        'displayName': place['displayName'],
                        'latitude': place['location']['latitude'],
                        'longitude': place['location']['longitude'],
                        'cuisine': place['cuisine'],
                        'rating': place.get('rating', 0),
                        'formattedAddress': place.get('formattedAddress', ''),
                        'distance': place['distance']
                    }
                    for place in filtered_results
                ],
                'google_maps_api_key': api_key
            }

            # Render the search results template with context
            return render(request, 'search/search_results.html', context)
        else:
            # Return an error response if location is not found
            return JsonResponse({'error': 'Location not found'}, status=400)

    except requests.RequestException as e:
        # Handle request exceptions
        return JsonResponse({'error': str(e)}, status=500)


# Function to calculate the distance between two lat/long points
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 3959  # Earth's radius in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(R * c, 1)


# Function to parse the primaryType (e.g., convert underscores to spaces)
def parse_underscore(text):
    if '_' in text:
        return ' '.join(text.split('_'))
    return text
