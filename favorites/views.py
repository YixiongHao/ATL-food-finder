from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Restaurant, UserProfile, Favorite
from django.shortcuts import render


# @login_required
# @csrf_exempt
def favorite_restaurant(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'You must be logged in to favorite a restaurant.'}, status=401)

    if request.method == 'POST':
        place_id = request.POST.get('place_id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')

        if not lat or not lng:
            return JsonResponse({'error': 'Missing latitude or longitude'}, status=400)

        # Check if the restaurant already exists, if not, create it
        restaurant, created = Restaurant.objects.get_or_create(
            place_id=place_id,
            defaults={'name': name, 'address': address, 'lat': lat, 'lng': lng}
        )

        # Create or get the favorite entry
        Favorite.objects.get_or_create(user=request.user, restaurant=restaurant, defaults={
            'title': name,
            'description': address,
            'distance': 0.0,  # Or however you want to handle this
            'cuisine': 'Unknown',  # Provide a default or adjust as needed
            'rating': 0.0,  # Or however you want to handle this
            'place_id': place_id
        })

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def user_favorites(request):
    if request.user.is_authenticated:
        # Use the correct relation to access favorites
        saved_restaurants = Restaurant.objects.filter(favorites__user=request.user).order_by('name')
        return render(request, 'favorites/favorites.html', {'saved_restaurants': saved_restaurants})
    else:
        return redirect('login')  # Redirect to login if not authenticated
