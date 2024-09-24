from django.http import JsonResponse
from django.views import View
from .models import Restaurant
from django.shortcuts import render, get_object_or_404
import json
import threading

# Threading lock ensures only one request is processed at a time.
# This prevents a bunch of errors from showing up on the run screen.
# ECE3058 clutch
lock = threading.Lock()

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

# Each Restaurant object has its own details page
# Should include:
# Name, address
# Type
# Short description (if possible)
# Reviews
# Option to add to favorites
# Google Map with one marker on restaurant
def restaurant_detail(request, place_id):
    restaurant = get_object_or_404(Restaurant, place_id=place_id)
    context = {
        'restaurant': restaurant
    }
    return render(request, 'details/restaurant_detail.html', context)

""" Previous code
........................................................................................................................
from django.shortcuts import render, redirect

from ATL_food_finder import settings
from .models import Restaurant
from .forms import RestaurantForm

def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'details/add_restaurant.html', {'form': form})

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'details/restaurant_list.html', {'details': restaurants})

def map(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key': key,
    }
    return render(request, 'details/base.html', context)
........................................................................................................................
"""