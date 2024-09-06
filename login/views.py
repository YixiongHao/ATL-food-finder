from django.shortcuts import render
from django.http import HttpResponse

from login.forms import LoginForm


# Create your views here.


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})