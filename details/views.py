from django.http import JsonResponse
from django.views import View
from ATL_food_finder import settings
from .models import Restaurant
from django.shortcuts import render, get_object_or_404
from urllib.parse import urlparse
import json
import threading
import requests

# Threading lock ensures only one request is processed at a time.
lock = threading.Lock()

# Google API key
GOOGLE_API_KEY = settings.GOOGLE_API_KEY

class SaveRestaurantsView(View):
    def post(self, request):
        with lock:
            data = request.POST.getlist('restaurants')  # Expecting a list of JSON strings
            for restaurant_data in data:
                # Parse the JSON string into a dictionary
                restaurant = json.loads(restaurant_data)

                name = restaurant['name']
                address = restaurant['address']
                lat = restaurant['geometry']['location']['lat']
                lng = restaurant['geometry']['location']['lng']
                place_id = restaurant['place_id']

                # Create or update the restaurant in the database
                Restaurant.objects.update_or_create(
                    place_id=place_id,
                    defaults={
                        'name': name,
                        'address': address,
                        'lat': lat,
                        'lng': lng
                    }
                )
        return JsonResponse({'status': 'success'})


# Function to get restaurant details from Google Places API, including contact info
def get_place_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('result')
    return None


# Function to calculate distance between user and restaurant
def calculate_distance(user_lat, user_lng, restaurant_lat, restaurant_lng):
    from math import radians, sin, cos, sqrt, atan2
    R = 6371  # Radius of the earth in km
    dlat = radians(restaurant_lat - user_lat)
    dlng = radians(restaurant_lng - user_lng)
    a = sin(dlat / 2) ** 2 + cos(radians(user_lat)) * cos(radians(restaurant_lat)) * sin(dlng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# Each Restaurant object has its own details page
def restaurant_detail(request, place_id):
    # Fetch restaurant details from Google Places API
    place_details = get_place_details(place_id)
    cuisine_type = request.GET.get('cuisine_type', '')

    if not place_details:
        return JsonResponse({'status': 'error', 'message': 'Details not found'}, status=404)

    # Attempt to get user location from the request
    user_lat = request.GET.get('lat')
    user_lng = request.GET.get('lng')

    if not user_lat or not user_lng:
        # Set to default location if user's lat/lng not provided
        user_lat, user_lng = 33.7488, -84.3877  # Example default (Atlanta)

    try:
        user_lat = float(user_lat)
        user_lng = float(user_lng)
    except (ValueError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid coordinates provided'}, status=400)

    # Prepare context for rendering
    context = {
        'restaurant': {
            'name': place_details.get('name'),
            'address': place_details.get('formatted_address'),
            'lat': place_details['geometry']['location']['lat'],
            'lng': place_details['geometry']['location']['lng'],
            'rating': place_details.get('rating'),
            'reviews': place_details.get('reviews', []),
            'phone': place_details.get('formatted_phone_number'),  # Phone number
            'email': f"info@{urlparse(place_details.get('website', '')).hostname if place_details.get('website') else 'example.com'}",
            'website': place_details.get('website'),  # Website URL
            'distance': calculate_distance(user_lat, user_lng, place_details['geometry']['location']['lat'], place_details['geometry']['location']['lng']),
        },
        'cuisine_type': cuisine_type,
        'GOOGLE_API_KEY': GOOGLE_API_KEY
    }

    return render(request, 'details/restaurant_detail.html', context)
