from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import googlemaps

# Create your views here.

def sign_in(request):
    key = settings.GOOGLE_API_KEY
    context = {
        "key": key,
    }
    return render(request, 'map/map.html', context)