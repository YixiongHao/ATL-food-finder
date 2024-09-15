from django.shortcuts import render
from .models import Favorite

# Create your views here.


def favorites(request):
    faves = Favorite.objects.all()
    context = {'faves': faves}
    return render(request, 'favorites/favorites.html', context)
