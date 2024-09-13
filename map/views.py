from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Create your views here.

# Directs user to the home map page. Passes the server's API key.
def sign_in(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key': key,
    }
    return render(request, 'map/map.html', context)