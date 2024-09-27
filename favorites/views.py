# views.py
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Favorite
from django.conf import settings



def add_favorite(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            place_id = data.get('place_id')
            name = data.get('name')
            if place_id:
                favorite, created = Favorite.objects.get_or_create(user=request.user, place_id=place_id, name=name)
                return JsonResponse({'success': created})  # Return success response
            else:
                return JsonResponse({'error': 'place_id is required'}, status=469)
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

@require_POST
def remove_favorite(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        place_id = data.get('place_id')
        name = data.get('name')

        if place_id:
            try:
                favorite = Favorite.objects.get(user=request.user, place_id=place_id, name=name)
                favorite.delete()  # Remove the favorite entry
                return JsonResponse({'success': True})  # Return success response
            except Favorite.DoesNotExist:
                return JsonResponse({'error': 'Favorite not found'}, status=404)
        else:
            return JsonResponse({'error': 'place_id is required'}, status=400)
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

def user_favorites(request):
    saved_restaurants = Favorite.objects.filter(user=request.user).order_by(
        'name')
    # print(saved_restaurants)
    key = settings.GOOGLE_API_KEY
    context = {
        'key': key,
        'saved_restaurants': saved_restaurants
    }
    return render(request, 'favorites/favorites.html', context)

def get_favorites(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('place_id', flat=True)
        return JsonResponse(list(favorites), safe=False)
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=403)