from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
from django.http import JsonResponse

# Create your views here.

# Directs user to the home map page. Passes the server's API key.
def sign_in(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key': key,
    }
    return render(request, 'map/map.html', context)

# def place_search(request):
#     query = request.GET.get('query')
#     location = request.GET.get('location')
#     radius = request.GET.get('radius')
#     api_key = settings.GOOGLE_API_KEY  # Use your API key from settings
#
#     if not query or not location or not radius:
#         return JsonResponse({'error': 'Query, location, and radius are required'}, status=400)
#
#     url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={location}&radius={radius}&key={api_key}'
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         return JsonResponse(response.json())
#     else:
#         return JsonResponse({'error': 'Error fetching data from Google Places API'}, status=response.status_code)