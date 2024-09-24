from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Restaurant, UserProfile

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

        # Associate the restaurant with the user's favorites
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.restaurant = restaurant
        user_profile.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'})