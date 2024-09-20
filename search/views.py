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

            radius = 1500  # placeholder
            # Use Google Places API to search for nearby restaurants
            query = request.GET.get('query', '')
            url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&radius={radius}&type=restaurant&keyword={query}&key={api_key}'
            response = requests.get(url)
            results = response.json().get('results', [])
            rich.print(results)
            context = {'results': results, 'google_maps_api_key': api_key}
            return render(request, 'search/search_results.html', context)
        else:
            return JsonResponse({'error': 'Location not found'}, status=400)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)